from stmpy import Driver
from groupState import GroupState, ASSIGN_TASK, DELETE_TASK, COMPLETE_TASK, START_TASK, TaskStatus, NO_TASKS, ASSIGNED, IN_PROGRESS
from time import sleep

driver = Driver()
groupname = "test"
g = GroupState(groupname, driver)
driver.start()

task = "t1"
# Test task_deleted_from_none
driver.send(DELETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == NO_TASKS
# Test task_started_from_none
driver.send(START_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == NO_TASKS
# Test task_completed_from_none
driver.send(COMPLETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == NO_TASKS
# Test task_assigned_from_none
driver.send(ASSIGN_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == ASSIGNED
assert g.tasks[task] == TaskStatus.ASSIGNED


# Test task_deleted_from_assigned
driver.send(DELETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == NO_TASKS
assert g.tasks.get(task) is None

driver.send(ASSIGN_TASK, groupname, [task])

# Test task_completed_from_assigned
driver.send(COMPLETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == ASSIGNED
assert g.tasks[task] == TaskStatus.ASSIGNED

# Test task_assigned_from_assigned
driver.send(ASSIGN_TASK, groupname, ["t2"])
sleep(0.01)
assert g.stm.state == ASSIGNED
assert g.tasks[task] == TaskStatus.ASSIGNED
assert g.tasks["t2"] == TaskStatus.ASSIGNED

driver.send(DELETE_TASK, groupname, ["t2"])
sleep(0.01)
assert g.stm.state == ASSIGNED
assert g.tasks[task] == TaskStatus.ASSIGNED
assert g.tasks.get("t2") is None

# Test task_started_from_assigned
driver.send(START_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == IN_PROGRESS
assert g.tasks[task] == TaskStatus.IN_PROGRESS

# Test task_assigned_from_progress
driver.send(ASSIGN_TASK, groupname, ["t2"])
sleep(0.01)
assert g.stm.state == IN_PROGRESS
assert g.tasks[task] == TaskStatus.IN_PROGRESS
assert g.tasks["t2"] == TaskStatus.ASSIGNED

# task_started_from_progress
driver.send(START_TASK, groupname, ["t2"])
sleep(0.01)
assert g.stm.state == IN_PROGRESS
assert g.tasks[task] == TaskStatus.IN_PROGRESS
assert g.tasks["t2"] == TaskStatus.IN_PROGRESS

# Test task_complete_from_progress (Can end up back in IN PROGRESS, ASSIGNED or NO TASK
# IN PROGRESS
driver.send(COMPLETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == IN_PROGRESS
assert g.tasks[task] == TaskStatus.COMPLETED
assert g.tasks["t2"] == TaskStatus.IN_PROGRESS

# NO TASK
driver.send(COMPLETE_TASK, groupname, ["t2"])
sleep(0.01)
assert g.stm.state == NO_TASKS
assert g.tasks[task] == TaskStatus.COMPLETED
assert g.tasks["t2"] == TaskStatus.COMPLETED

# ASSIGNED
g.tasks.pop(task)
g.tasks.pop("t2")
driver.send(ASSIGN_TASK, groupname, [task])
driver.send(ASSIGN_TASK, groupname, ["t2"])
driver.send(START_TASK, groupname, [task])
driver.send(COMPLETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == ASSIGNED
assert g.tasks[task] == TaskStatus.COMPLETED
assert g.tasks["t2"] == TaskStatus.ASSIGNED

# Test task_deleted_from_progress can end up in IN PROGRESS, NO TASK or ASSIGNED
g.tasks[task] = TaskStatus.ASSIGNED
driver.send(START_TASK, groupname, [task])
driver.send(START_TASK, groupname, ["t2"])

# IN PROGRESS
driver.send(DELETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == IN_PROGRESS
assert g.tasks.get(task) is None
assert g.tasks["t2"] == TaskStatus.IN_PROGRESS

# NO TASK
driver.send(DELETE_TASK, groupname, ["t2"])
sleep(0.01)
assert g.stm.state == NO_TASKS
assert g.tasks.get("t2") is None

# ASSIGNED
driver.send(ASSIGN_TASK, groupname, [task])
driver.send(ASSIGN_TASK, groupname, ["t2"])
driver.send(START_TASK, groupname, [task])
driver.send(DELETE_TASK, groupname, [task])
sleep(0.01)
assert g.stm.state == ASSIGNED
assert g.tasks.get(task) is None
assert g.tasks["t2"] == TaskStatus.ASSIGNED




driver.stop()