import {browser} from "$app/environment";
import { groupStore } from "./stores";

async function fetchGroups() {
    if (browser) {
        const res =
            await fetch('http://localhost:3000/groups', {
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
