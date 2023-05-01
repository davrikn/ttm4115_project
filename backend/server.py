from stmpy import Driver
from flask import Flask, request
import paho.mqtt.client as mqtt
from MqttClient import get
from groupState import GroupState, ASSIGN_TASK, DELETE_TASK, COMPLETE_TASK, START_TASK, TaskStatus
from helpQueueState import HelpQueueState, REQUEST_HELP, FINISH_HELP, START_HELP
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from os import environ
from flask_cors import CORS
from datetime import timedelta

environ['host'] = "wirelogger.com"

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "SomeBigSecret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
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
    pass


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
    return {name: group.state() for (name, group) in groups.items()}

@app.route("/groups/<groupname>", methods=["GET"])
def get_group_state(groupname):
    if groupname not in groups.keys():
        return f"Group {groupname} not found", 404

    # Taskstate enum: 1 = Assigned, 2 = In progress, 3 = Complete
    # {"taskname": TaskState enum}
    return groups[groupname].state()


@app.route("/groups/<groupname>/tasks/<taskname>/start", methods=["GET"])
@jwt_required()
def start_task(groupname, taskname):
    identity = get_jwt_identity()
    username = identity["username"]

    if groupname not in groups.keys():
        return f"Group {groupname} not found", 404
    if taskname not in tasks.keys():
        return f"Task {taskname} not found", 404
    if username not in groups[groupname].members:
        return f"User {username} is not a member of group {groupname}", 403
    if groups[groupname].tasks[taskname] != TaskStatus.ASSIGNED:
        return f"Cannot start task that isn't assigned", 409

    driver.send(START_TASK, groupname, [taskname])
    client.client.publish(f"groups/{groupname}/status", str(groups[groupname].status()))
    return "Task started", 200


@app.route("/groups/<groupname>/tasks/<taskname>/finish", methods=["GET"])
@jwt_required()
def finish_task(groupname, taskname):
    identity = get_jwt_identity()
    username = identity["username"]

    if groupname not in groups.keys():
        return f"Group {groupname} not found", 404
    if taskname not in tasks.keys():
        return f"Task {taskname} not found", 404
    if username not in groups[groupname].members:
        return f"User {username} is not a member of group {groupname}", 403
    if groups[groupname].tasks[taskname] != TaskStatus.IN_PROGRESS:
        return f"Cannot complete task that isn't in progress", 409

    driver.send(COMPLETE_TASK, groupname, [taskname])
    client.client.publish(f"groups/{groupname}/status", str(groups[groupname].status()))
    return "Task finished", 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    # {"taskname": "taskdescription"}
    return tasks


@app.route('/help', methods=["GET"])
def get_queue():
    # {"receiving": string[], "awaiting": string[]}
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
    return f"You are {len(queue.in_help)} in line"


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
    group = GroupState(groupname, driver)
    groups[groupname] = group
    for task in tasks.keys():
        driver.send(ASSIGN_TASK, groupname, [task])
    return f"Group {groupname} successfully created", 200

@app.route("/groups/<groupname>/members", methods=["GET"])
def get_groupmembers(groupname):
    if groupname not in groups.keys():
        return f"Group {groupname} not found", 404
    return groups[groupname].members, 200


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
