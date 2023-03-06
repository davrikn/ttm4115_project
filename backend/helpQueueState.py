from stmpy import Machine, Driver
import paho.mqtt.client as mqtt_client

init_state = {'source': 'initial', 'target': 'idle'}
receive_request = {'trigger': 'request_help', 'source': 'idle', 'target': 'helping', 'effect': 'enqueue(*)'}
next_help = {'trigger': 'next_help', 'source': 'helping', 'target': 'helping', 'effect': 'dequeue'}
finish_help = {'trigger': 'finish_help', 'source': 'helping', 'target': 'idle'}


class HelpQueueState:

    def __init__(self, client: mqtt_client.Client):
        self.mqtt = client
        self.stm = Machine("Helpqueue", [init_state, receive_request, next_help, finish_help], self)
        self.queue = []

    def enqueue(self, group: str):
        self.queue.append(group)

    def dequeue(self):
        self.queue.pop()
        self.mqtt.publish('help/update', payload=str(self))
        if len(self.queue) == 0:
            self.stm.send('finish_help')

    def __str__(self):
        return "Currently queue length: {}".format(len(self.queue))