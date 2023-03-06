from stmpy import Machine, Driver
import paho.mqtt.client as mqtt_client

init_state = {'source': 'initial', 'target': 'working'}
proceed = {'source': 'working', 'target': 'working', 'effect': 'proceed'}
request_help = {'source': 'working', 'target': 'await_help', 'effect': 'request_help'}
get_help = {'source': 'working', 'target': 'working'}

class GroupState:
    task = 0

    def __init__(self, name: str, driver: Driver, mqtt: mqtt_client.Client):
        self.mqtt = mqtt
        self.name = name
        self.stm = Machine(name, [init_state, proceed], self)
        driver.add_machine(self.stm)

    def proceed(self):
        self.task += 1

    def request_help(self):
        txt = "help/request/{}"
        self.mqtt.publish(txt.format(self.name))

    def __str__(self):
        return "Group: {}, task: {}".format(self.name, self.task)