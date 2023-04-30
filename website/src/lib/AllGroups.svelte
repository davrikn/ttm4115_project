<script>
    import Group from '$lib/Group.svelte';
    import {browser} from "$app/environment";

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

    async function getGroups() {
        const groupsJSON = await fetchGroups()
        const groups = []
        for (const [name, tasks] of Object.entries(groupsJSON)) {
            groups.push({name: name, tasks: tasks})
        }
        console.log(groups)
        return groups
    }
</script>

<div class="groups">
    {#await getGroups()}
        <p>loading...</p>
    {:then groups}
        {#each groups as group}
            <Group name={group.name} tasks={group.tasks}/>
        {/each}
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}
</div>

<style>
    .groups {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
</style>
