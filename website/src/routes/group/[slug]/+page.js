// A function that returns a group number as slug in sveltekit
// https://kit.svelte.dev/docs#routing-advanced-dynamic-routes
import {browser} from "$app/environment";
export function load({ params }) {
	return {
		slug: params.slug,
		tasks: updateGroupTasks(params.slug)
	};
}



async function updateGroupTasks(groupname) {
	if (browser) {
		const tasksJSON = await fetchGroupTasks(groupname)
		const tasks = []
		for (const [taskname, status] of Object.entries(tasksJSON)) {
			tasks.push({taskname: taskname, status: status})
		}
		console.log("TASKS!!", tasks)
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
