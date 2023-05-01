from stmpy import Machine, Driver
from time import sleep
from enum import IntEnum
from functools import reduce

############################################################################################
#                                       TRIGGERS                                           #
############################################################################################
ASSIGN_TASK = 'assign_task'
DELETE_TASK = 'delete_task'
TASKS_ASSIGNED = 'tasks_assigned'
TASKS_NOT_ASSIGNED = 'tasks_not_assigned'
TASK_IN_PROGRESS = 'task_in_progress'
TASK_NOT_IN_PROGRESS = 'task_not_in_progress'
COMPLETE_TASK = 'task_done'
START_TASK = 'start_task'

############################################################################################
#                                         STATES                                           #
############################################################################################

NO_TASKS = 'no_tasks'
ASSIGNED = 'task_assigned'
VALIDATE_ASSIGNED = 'validate_assigned'
VALIDATE_PROGRESS = 'validate_in_progress'
IN_PROGRESS = 'in_progress'

no_tasks = {"name": NO_TASKS}
assigned = {"name": ASSIGNED}
validate_assigned = {"name": VALIDATE_ASSIGNED, ASSIGN_TASK: 'defer', DELETE_TASK: 'defer', COMPLETE_TASK: 'defer', START_TASK: 'defer', 'entry': 'validate_assigned()'}
validate_progress = {"name": VALIDATE_PROGRESS, ASSIGN_TASK: 'defer', DELETE_TASK: 'defer', COMPLETE_TASK: 'defer', START_TASK: 'defer', 'entry': 'validate_in_progress()'}
in_progress = {"name": IN_PROGRESS}

############################################################################################
#                                     TRANSITIONS                                          #
############################################################################################
init_state = {'source': 'initial', 'target': NO_TASKS}

# Out from no tasks
task_assigned_from_none = {'source': NO_TASKS, 'trigger': ASSIGN_TASK, 'target': ASSIGNED, 'effect': 'add_task(*)'}
task_deleted_from_none = {'source': NO_TASKS, 'trigger': DELETE_TASK, 'target': NO_TASKS}
task_started_from_none = {'source': NO_TASKS, 'trigger': START_TASK, 'target': NO_TASKS}
task_completed_from_none = {'source': NO_TASKS, 'trigger': COMPLETE_TASK, 'target': NO_TASKS}

# Out from task assigned
task_deleted_from_assigned = {'source': ASSIGNED, 'trigger': DELETE_TASK, 'target': VALIDATE_ASSIGNED, 'effect': 'delete_task(*)'}
task_started_from_assigned = {'source': ASSIGNED, 'trigger': START_TASK, 'target': IN_PROGRESS, 'effect': 'start_task(*)'}
task_assigned_from_assigned = {'source': ASSIGNED, 'trigger': ASSIGN_TASK, 'target': ASSIGNED, 'effect': 'add_task(*)'}
task_completed_from_assigned = {'source': ASSIGNED, 'trigger': COMPLETE_TASK, 'target': ASSIGNED}

# Out from in progress
task_complete_from_progress = {'source': IN_PROGRESS, 'trigger': COMPLETE_TASK, 'target': VALIDATE_PROGRESS, 'effect': 'complete_task(*)'}
task_assigned_from_progress = {'source': IN_PROGRESS, 'trigger': ASSIGN_TASK, 'target': IN_PROGRESS, 'effect': 'add_task(*)'}
task_deleted_from_progress = {'source': IN_PROGRESS, 'trigger': DELETE_TASK, 'target': VALIDATE_PROGRESS, 'effect': 'delete_task(*)'}
task_started_from_progress = {'source': IN_PROGRESS, 'trigger': START_TASK, 'target': IN_PROGRESS, 'effect': 'start_task(*)'}

# Out from validating progress
no_task_in_progress = {'source': VALIDATE_PROGRESS, 'trigger': TASK_NOT_IN_PROGRESS, 'target': VALIDATE_ASSIGNED}
task_in_progress = {'source': VALIDATE_PROGRESS, 'trigger': TASK_IN_PROGRESS, 'target': IN_PROGRESS}

# Out from validating assigned
task_assigned = {'source': VALIDATE_ASSIGNED, 'trigger': TASKS_ASSIGNED, 'target': ASSIGNED}
no_task_assigned = {'source': VALIDATE_ASSIGNED, 'trigger': TASKS_NOT_ASSIGNED, 'target': NO_TASKS}


class TaskStatus(IntEnum):
    ASSIGNED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class GroupState:
    def __init__(self, name: str, driver: Driver):
        self.name = name
        self.tasks = dict()
        self.stm = Machine(name=name, transitions=[init_state, task_assigned_from_none, task_deleted_from_none, task_started_from_none, task_completed_from_none, task_deleted_from_assigned, task_started_from_assigned, task_assigned_from_assigned, task_completed_from_assigned,
                                                   task_complete_from_progress, task_assigned_from_progress, task_deleted_from_progress, task_started_from_progress, no_task_in_progress, task_in_progress, task_assigned, no_task_assigned],
                           states=[no_tasks, assigned, validate_assigned, validate_progress, in_progress], obj=self)
        driver.add_machine(self.stm)
        self.members = []

    def add_member(self, uname: str):
        if uname not in self.members:
            self.members.append(uname)

    def remove_member(self, uname: str):
        if uname in self.members:
            self.members.remove(uname)

    def validate_assigned(self):
        for task in self.tasks.values():
            if task == TaskStatus.ASSIGNED:
                self.stm.send(TASKS_ASSIGNED)
                return
        self.stm.send(TASKS_NOT_ASSIGNED)

    def validate_in_progress(self):
        for task in self.tasks.values():
            if task == TaskStatus.IN_PROGRESS:
                self.stm.send(TASK_IN_PROGRESS)
                return
        self.stm.send(TASK_NOT_IN_PROGRESS)

    def add_task(self, task: str):
        self.tasks[task] = TaskStatus.ASSIGNED

    def start_task(self, task: str):
        self.tasks[task] = TaskStatus.IN_PROGRESS

    def complete_task(self, task: str):
        self.tasks[task] = TaskStatus.COMPLETED

    def delete_task(self, task: str):
        self.tasks.pop(task)


    def completed_tasks(self):
        i = 0
        for task in self.tasks.values():
            if task == TaskStatus.COMPLETED:
                i += 1
        return i

    def in_progress_tasks(self):
        i = 0
        for task in self.tasks.values():
            if task == TaskStatus.IN_PROGRESS:
                i += 1
        return i

    def assigned_tasks(self):
        i = 0
        for task in self.tasks.values():
            if task == TaskStatus.ASSIGNED or TaskStatus.IN_PROGRESS:
                i += 1
        return i

    def state(self):
        return {key: int(value) for key, value in self.tasks.items()}

    def __str__(self):
        return f"Group: {self.name}\nAssigned tasks: {self.assigned_tasks()}\nTasks in progress: {self.in_progress_tasks()}\nTasks complete: {self.completed_tasks()}"

if __name__ == '__main__':
    driver = Driver()
    g = GroupState('G1', driver)

    driver.start(keep_active=True)

    print(g.stm.state)
    g.stm.send(ASSIGN_TASK, args=['task1'])
    sleep(0.1)
    print(g.stm.state)
    g.stm.send(START_TASK, args=['task1'])
    sleep(0.1)
    print(g)
    print(g.stm.state)
    g.stm.send(COMPLETE_TASK, args=['task1'])
    sleep(0.1)
    print(g)
    driver.stop()
