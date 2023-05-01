import {browser} from "$app/environment";
export const ssr = false
export async function load({params}) {
    return {
        queue: await updateHelpQueue(),
    };
}

async function updateHelpQueue() {
    if (browser) {
        const res = await fetch(`http://localhost:3000/help`, {
            method: 'GET', headers: {
                'Content-Type': 'application/json'
            },
        })
        const queue = await res.json()
        if (res.ok) {
            return queue
        } else {
            throw new Error(await res.text())
        }
    }
}
