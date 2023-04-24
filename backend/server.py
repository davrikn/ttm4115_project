from stmpy import Driver
from flask import Flask, request
import paho.mqtt.client as mqtt
from MqttClient import get
from groupState2 import GroupState2, ASSIGN_TASK, DELETE_TASK, COMPLETE_TASK, START_TASK
import json
from helpQueueState import HelpQueueState, REQUEST_HELP, FINISH_HELP, START_HELP
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


host = "wirelogger.com"

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "SomeBigSecret"
jwt = JWTManager(app)

driver = Driver()
driver.start(keep_active=True)
queue = HelpQueueState(driver)
client = get()

groups = dict()
tasks = dict()
users = {
    "David": {"password": "David123!"},
    "Ola": {"password": "Ola123!"},
    "Emil": {"password": "Emil123!"},
    "Helene": {"password": "Helene123!"},
    "Sander": {"password": "Sander123!"},
    "Admin": {"password": "Admin123!", "claim": "admin"}
}

def handle_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    topic_parts = message.topic.split('/')

    if topic_parts[0] == 'group':
        handle_group_messages(topic_parts[2], topic_parts[1], message.payload)
    elif topic_parts[0] == 'help':
        handle_help(topic_parts[1], message.payload)

def handle_help(group, payload):

    # TODO: implement
    pass


def handle_group_messages(event, group, payload):
    if groups.get(group) is None:
        return

    if event == "startTask":
        payload = json.loads(payload)
        taskname = payload['task']
        driver.send(START_TASK, group, [taskname])
    elif event == 'finishTask':
        payload = json.loads(payload)
        taskname = payload['task']
        driver.send(COMPLETE_TASK, group, [taskname])


@app.route("/login", methods=["POST"])
def login():
    uname = request.json.get("username")
    password = request.json.get("password")

    user = users.get(uname)
    if user is None:
        return f"User {uname} not found", 404
    if password != user["password"]:
        return f"Wrong password", 401

    token = create_access_token({"username": uname, "claim": user.get("claim") or "user"})
    return {"access_token": token}

@app.route("/groups", methods=["GET"])
def get_groups():
    return list(groups.keys())

@app.route("/groups/<groupname>", methods=["GET"])
def get_group_state(groupname):
    if groupname in groups.keys():
        return groups[groupname].state()
    else:
        return f"Group {groupname} not found", 404

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return tasks

@app.route('/help', methods=["GET"])
def get_queue():
    return queue.state()

@app.route('/help/request', methods=["POST"])
@jwt_required()
def request_help():
    groupname = request.json.get('groupname')
    identity = get_jwt_identity()
    uname = identity['username']
    if groups.get(groupname) is None:
        return f"Group {groupname} not found", 404
    if uname not in groups[groupname].members:
        return f"User {uname} is not in group {groupname}", 403
    driver.send(REQUEST_HELP, 'Helpqueue', [groupname])
    client.client.publish('help/status', str(queue.state()))
    return f"You are {len(queue.in_help) - 1} in line"


@app.route('/help/start', methods=["POST"])
@jwt_required()
def start_help():
    groupname = request.json.get('groupname')
    identity = get_jwt_identity()
    if identity['claim'] != 'admin':
        return f"User can not update helpqueue", 403

    if groupname not in queue.queue:
        return f"Group {groupname} has not requested help", 400

    driver.send(START_HELP, 'Helpqueue', [groupname])
    client.client.publish('help/status', str(queue.state()))
    return f"Help started for group {groupname}"


@app.route('/help/finish', methods=["POST"])
@jwt_required()
def stop_help():
    groupname = request.json.get('groupname')
    identity = get_jwt_identity()
    if identity['claim'] != 'admin':
        return f"User can not update helpqueue", 403

    if groupname not in queue.in_help:
        return f"Group {groupname} is not currently being helped", 400

    driver.send(FINISH_HELP, 'Helpqueue', [groupname])
    client.client.publish('help/status', str(queue.state()))
    return f"Help finished for group {groupname}"


@app.route("/groups", methods=["POST"])
@jwt_required()
def create_group():
    identity = get_jwt_identity()
    if identity["claim"] != "admin":
        return f"User does not have the right to create groups", 403
    groupname = request.json.get("groupname")
    if groupname in groups.keys():
        return "Group already exists", 400
    if groupname == "Helpqueue":
        return "Groupname Helpqueue is not allowed", 400
    client.client.publish("groupCreated", str({"groupname": groupname}))
    group = GroupState2(groupname, driver)
    groups[groupname] = group
    for task in tasks.keys():
        driver.send(ASSIGN_TASK, ASSIGN_TASK, [task])
    return f"Group {groupname} successfully created", 200

@app.route("/groups/<groupname>/members", methods=["POST"])
@jwt_required()
def add_groupmember(groupname):
    identity = get_jwt_identity()
    if identity["claim"] != "admin":
        return f"User does not have the right to add members to groups", 403

    uname = request.json.get("username")
    if uname not in users.keys():
        return f"User {uname} not found", 404
    if groupname not in groups.keys():
        return f"Group {groupname} not found", 404
    groups[groupname].add_member(uname)
    return f"User {uname} successfully added to group {groupname}", 200


@app.route("/groups/<groupname>/members", methods=["DELETE"])
@jwt_required()
def remove_groupmember(groupname):
    identity = get_jwt_identity()
    if identity["claim"] != "admin":
        return f"User does not have the right to remove members from groups", 403

    uname = request.json.get("username")
    if uname not in users.keys():
        return f"User {uname} not found", 404
    if groupname not in groups.keys():
        return f"Group {groupname} not found", 404
    groups[groupname].remove_member(uname)
    return f"User {uname} successfully removed from group {groupname}", 200

@app.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    identity = get_jwt_identity()
    if identity["claim"] != "admin":
        return f"User does not have the right to create groups", 403
    taskname, task = request.json.get("taskname"), request.json.get("task")
    if taskname in tasks.keys():
        return f"Task {taskname} already exists", 409
    tasks[taskname] = task
    for group in groups.keys():
        driver.send(ASSIGN_TASK, group, [taskname])
    return f"Task {taskname} added"


@app.route("/tasks/<taskname>", methods=["DELETE"])
@jwt_required()
def remove_task(taskname):
    identity = get_jwt_identity()
    if identity["claim"] != "admin":
        return f"User does not have the right to create groups", 403
    if not taskname in tasks.keys():
        return
    tasks.pop(taskname)
    for group in groups.keys():
        driver.send(DELETE_TASK, group, [taskname])
    return f"Task {taskname} removed"


client.set_on_message(handle_message)
app.run(port=3000)
