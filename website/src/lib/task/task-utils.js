import {browser} from "$app/environment";
import {taskStore} from "$lib/stores.js";



async function fetchTasks() {
    if (browser) {
        const res =
            await fetch('http://localhost:3000/tasks', {
                method: 'GET',
                headers: {
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
export async function updateTasks() {
    if (browser) {
        const tasksJSON = await fetchTasks()
        const tasks = []
        for (const [taskname, task] of Object.entries(tasksJSON)) {
            tasks.push({taskname: taskname, task: task})
        }
        taskStore.set(tasks)
        return tasks
    }
}
