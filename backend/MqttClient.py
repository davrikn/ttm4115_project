import paho.mqtt.client as mqtt
from time import sleep
import json
from typing import Callable, Any, TypeVar

Instance = TypeVar("MqttClient", bound="MqttClient")


def get():
    if MqttClient.instance is None:
        MqttClient.instance = MqttClient()
    return MqttClient.instance


class MqttClient():
    instance: Instance = None

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.default_on_message
        self.client.connect("wirelogger.com")
        self.client.subscribe('#')
        self.client.loop_start()

    def set_on_message(self, om: Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]):
        self.client.on_message = om

    def default_on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        print(msg.topic)
        print(json.loads(msg.payload))

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
