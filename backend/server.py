from groupState import  GroupState
from helpQueueState import HelpQueueState
from stmpy import Driver
from flask import Flask
import paho.mqtt.client as mqtt

host = "wirelogger.com"

app = Flask(__name__)

driver = Driver()
client = mqtt.Client()
client.connect(host)

helpQueue = HelpQueueState(client)
groups = []

def handle_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    messageKind = message.topic.split('/')[0]

    if messageKind == "help":
        messageKind2 = message.topic.split('/')[1]
        if messageKind2 == 'request':
            groupname = message.topic.split('/')[2]
            driver.send('request_help', 'Helpqueue', groupname)
    elif messageKind == "progress":
        groupname = message.topic.split('/')[1]
        driver.send('progress', groupname)
    elif messageKind == "create":
        groupname = message.topic.split('/')[1]
        groups.append(groupname)
        gs = GroupState(groupname, driver, client)
    else:
        ## TODO: Handle (or ignore) invalid topic
        pass

client.on_message(handle_message)


@app.route("/groups")
def get_groups():
    return str(groups)