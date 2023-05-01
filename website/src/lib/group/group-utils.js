import {browser} from "$app/environment";
import {groupStore} from "../stores.js";
import {invalidateAll} from "$app/navigation";

async function fetchGroups() {
    if (browser) {
        const res = await fetch('http://localhost:3000/groups', {
            method: 'GET', headers: {
                'Content-Type': 'application/json'
            },
        })
        const groups = await res.json()
        if (res.ok) {
            return groups
        } else {
            throw new Error(await res.text())
        }
    }
}


export async function updateGroups() {
    if (browser) {
        const groupsJSON = await fetchGroups()
        const groups = []
        for (const [name, tasks] of Object.entries(groupsJSON)) {
            groups.push({name: name, tasks: tasks})
        }
        groupStore.set(groups)
        return groups
    }
}


function startTask(groupname, taskname) {
    if (browser) {
        fetch(`http://localhost:3000/groups/${groupname}/tasks/${taskname}/start`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`

            },
        })
            .then((response) => response.text())
            .then((text) => {
                alert(text)
            })
            .catch((err) => {
                alert(err);
            });
    }
}

function finishTask(groupname, taskname) {
    if (browser) {
        fetch(`http://localhost:3000/groups/${groupname}/tasks/${taskname}/finish`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`

            },
        })
            .then((response) => response.text())
            .then((text) => {
                alert(text)
            })
            .catch((err) => {
                alert(err);
            });
    }
}


export function updateTaskStatus(groupname, taskname, status) {
    switch (status) {
        case 2:
            startTask(groupname, taskname)
            break;
        case 3:
            finishTask(groupname, taskname)
            break;
    }
    invalidateAll()
}

export async function updateGroupTasks(groupname) {
    if (browser) {
        const tasksJSON = await fetchGroupTasks(groupname)
        const tasks = []
        for (const [taskname, status] of Object.entries(tasksJSON)) {
            tasks.push({taskname: taskname, status: status})
        }

        return tasks
    }
}

async function fetchGroupTasks(groupname) {
    if (browser) {
        const res = await fetch(`http://localhost:3000/groups/${groupname}`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json'
            },
        })
        const groups = await res.json()
        if (res.ok) {
            return groups
        } else {
            throw new Error(await res.text())
        }
    }
}
