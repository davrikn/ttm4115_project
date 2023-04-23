from stmpy import Driver
from flask import Flask, request
import paho.mqtt.client as mqtt
from MqttClient import get
from groupState2 import GroupState2, ASSIGN_TASK, DELETE_TASK, COMPLETE_TASK, START_TASK
import json
from helpQueueState import HelpQueueState

host = "wirelogger.com"

app = Flask(__name__)

driver = Driver()
driver.start(keep_active=True)
client = get()

groups = dict()
tasks = dict()

def handle_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    topic_parts = message.topic.split('/')

    if topic_parts[0] == 'group':
        handle_group_messages(topic_parts[2], topic_parts[1], message.payload)
    elif topic_parts[0] == 'createGroup':
        handle_create_group(message.payload)
    elif topic_parts[0] == 'newTask':
        handle_new_task(message.payload)
    elif topic_parts[0] == 'deleteTask':
        handle_delete_task(message.payload)
    elif topic_parts[0] == 'help':
        handle_help(topic_parts[1], message.payload)

def handle_help(group, payload):
    # TODO: implement
    pass


def handle_group_messages(event, group, payload):
    if groups.get(group) is None:
        return
    payload = json.loads(payload)
    taskname = payload['task']

    if event == "startTask":
        driver.send(START_TASK, group, [taskname])
    elif event == 'finishTask':
        driver.send(COMPLETE_TASK, group, [taskname])


def handle_delete_task(payload):
    payload = json.loads(payload)
    taskname = payload["taskname"]
    if not taskname in tasks.keys():
        return
    tasks.pop(taskname)
    for group in groups.keys():
        driver.send(DELETE_TASK, group, [taskname])


def handle_new_task(payload):
    payload = json.loads(payload)
    taskname, task = payload["taskname"], payload["task"]
    if taskname in tasks.keys():
        return
    tasks[taskname] = task
    for group in groups.keys():
        driver.send(ASSIGN_TASK, group, [taskname])


def handle_create_group(payload):
    payload = json.loads(payload)
    groupname = payload["groupname"]
    if groupname in groups:
        return
    groupstate = GroupState2(groupname, driver)
    groups[groupname] = groupstate
    for task in tasks.keys():
        driver.send(ASSIGN_TASK, ASSIGN_TASK, [task])


@app.route("/groups")
def get_groups():
    return list(groups.keys())

@app.route("/groups/<groupname>")
def get_group_state(groupname):
    return groups[groupname].state()

@app.route("/tasks")
def get_tasks():
    return tasks

@app.route("/shutdown")
def shutdown():
    driver.stop()
    exit(0)



client.set_on_message(handle_message)
app.run(port=3000)
