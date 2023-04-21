from stmpy import Machine, Driver
from time import sleep

# States
NO_TASKS = 'no_tasks'
ASSIGNED = 'task_assigned'
VALIDATE_ASSIGNED = 'validate_assigned'
VALIDATE_PROGRESS = 'validate_in_progress'
IN_PROGRESS = 'in_progress'


# Triggers
ASSIGN_TASK = 'assign_task'
DELETE_TASK = 'delete_task'
TASKS_ASSIGNED = 'tasks_assigned'
TASKS_NOT_ASSIGNED = 'tasks_not_assigned'
TASK_IN_PROGRESS = 'task_in_progress'
TASK_NOT_IN_PROGRESS = 'task_not_in_progress'
TASK_DONE = 'task_done'
START_TASK = 'start_task'



init_state = {'source': 'initial', 'target': NO_TASKS}

# Out from no tasks
task_assigned_from_none = {'source': NO_TASKS, 'trigger': ASSIGN_TASK, 'target': ASSIGNED, 'effect': 'add_task(*)'}

# Out from task assigned
task_deleted = {'source': ASSIGNED, 'trigger': DELETE_TASK, 'target': VALIDATE_ASSIGNED, 'effect': 'validate_assigned()'}
task_started = {'source': ASSIGNED, 'trigger': START_TASK, 'target': IN_PROGRESS, 'effect': 'start_task(*)'}

# Out from in progress
task_complete = {'source': IN_PROGRESS, 'trigger': TASK_DONE, 'target': VALIDATE_PROGRESS, 'effect': 'complete_task(*); validate_in_progress()'}

# Out from validating progress
no_task_in_progress = {'source': VALIDATE_PROGRESS, 'trigger': TASK_NOT_IN_PROGRESS, 'target': VALIDATE_ASSIGNED, 'effect': 'validate_assigned()'}
task_in_progress = {'source': VALIDATE_PROGRESS, 'trigger': TASK_IN_PROGRESS,'target': IN_PROGRESS}

# Out from validating assigned
task_assigned = {'source': VALIDATE_ASSIGNED, 'trigger': TASKS_ASSIGNED, 'target': ASSIGNED}
no_task_assigned = {'source': VALIDATE_ASSIGNED, 'trigger': TASKS_NOT_ASSIGNED, 'target': NO_TASKS}

class GroupState2:
    def __init__(self, name: str, driver: Driver):
        self.tasks = []
        self.in_progress = []
        self.stm = Machine(name=name, transitions=[init_state,
                                  task_assigned_from_none,
                                  task_deleted,
                                  task_started,
                                  task_complete,
                                  no_task_in_progress,
                                  task_in_progress,
                                  task_assigned,
                                  no_task_assigned
                                  ], obj=self)
        driver.add_machine(self.stm)

    def add_task(self, task: str):
        self.tasks.append(task)

    def validate_assigned(self):
        if len(self.tasks) == 0:
            self.stm.send(TASKS_NOT_ASSIGNED)
        else:
            self.stm.send(TASKS_ASSIGNED)

    def validate_in_progress(self):
        if len(self.in_progress) == 0:
            self.stm.send(TASK_NOT_IN_PROGRESS)
        else:
            self.stm.send(TASK_IN_PROGRESS)

    def start_task(self, task: str):
        self.in_progress.append(task)

    def complete_task(self, task: str):
        self.in_progress.remove(task)
        self.tasks.remove(task)

if __name__ == '__main__':
    driver = Driver()
    g = GroupState2('G1', driver)

    driver.start(keep_active=True)

    print(g.stm.state)
    g.stm.send(ASSIGN_TASK, args=['task1'])
    sleep(0.1)
    print(g.stm.state)
    g.stm.send(START_TASK, args=['task1'])
    sleep(0.1)
    print(g.stm.state)
    g.stm.send(TASK_DONE, args=['task1'])
    sleep(0.1)
    print(g.stm.state)
    driver.stop()
