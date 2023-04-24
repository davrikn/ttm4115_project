from stmpy import Machine, Driver
import paho.mqtt.client as mqtt_client
from time import sleep

############################################################################################
#                                       TRIGGERS                                           #
############################################################################################

REQUEST_HELP = "request_help"
FINISH_HELP = "finish_help"
QUEUE_EMPTY = "queue_empty"
QUEUE_NOT_EMPTY = "queue_not_empty"

############################################################################################
#                                         STATES                                           #
############################################################################################

IDLE = "idle"
HELPING = "helping"
VALIDATE_QUEUE = "validate_queue"

idle = {'name': IDLE}
helping = {'name': HELPING}
validate_queue = {"name": VALIDATE_QUEUE, 'entry': 'validate_queue()', REQUEST_HELP: 'defer', FINISH_HELP: 'defer'}

############################################################################################
#                                     TRANSITIONS                                          #
############################################################################################
init_state = {'source': 'initial', 'target': IDLE}
finish_help_from_idle = {'source': IDLE, 'trigger': FINISH_HELP, 'target': IDLE}
request_help_from_idle = {'source': IDLE, 'trigger': REQUEST_HELP, 'target': HELPING, 'effect': 'enqueue(*)'}

finish_help_from_helping = {'source': HELPING, 'trigger': FINISH_HELP, 'target': VALIDATE_QUEUE, 'effect': 'dequeue(*)'}
request_help_from_helping = {'source': HELPING, 'trigger': REQUEST_HELP, 'target': HELPING, 'effect': 'enqueue(*)'}

queue_empty_from_validating = {'source': VALIDATE_QUEUE, 'trigger': QUEUE_EMPTY, 'target': IDLE}
queue_not_empty_from_validating = {'source': VALIDATE_QUEUE, 'trigger': QUEUE_NOT_EMPTY, 'target': HELPING}


class HelpQueueState:

    def __init__(self, driver: Driver):
        self.stm = Machine("Helpqueue", [init_state, finish_help_from_idle, request_help_from_idle, finish_help_from_helping,
                                         request_help_from_helping, queue_empty_from_validating, queue_not_empty_from_validating],
                           self, [idle, helping, validate_queue])
        self.queue = []
        driver.add_machine(self.stm)

    def enqueue(self, group: str):
        if group not in self.queue:
            self.queue.append(group)

    def dequeue(self, group: str):
        if group in self.queue:
            self.queue.pop()

    def validate_queue(self):
        if len(self.queue) == 0:
            self.stm.send(QUEUE_EMPTY)
        else:
            self.stm.send(QUEUE_NOT_EMPTY)

    def __str__(self):
        return "Currently queue length: {}".format(len(self.queue))

if __name__ == "__main__":
    d = Driver()
    q = HelpQueueState(d)

    d.start()

    d.send(REQUEST_HELP, 'Helpqueue', ['G1'])
    sleep(0.01)
    assert q.stm.state == HELPING
    assert q.queue[0] == 'G1'

    d.send(FINISH_HELP, 'Helpqueue', ['G1'])
    sleep(0.01)
    assert q.stm.state == IDLE
    assert len(q.queue) == 0

    d.stop()
