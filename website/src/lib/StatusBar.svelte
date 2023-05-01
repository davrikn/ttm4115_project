<script>

    import {groupStore, taskStore} from "$lib/stores.js";
    import {updateGroupTasks} from "$lib/group/group-utils.js";
    import {onMount} from "svelte";
    import {updateTasks} from "$lib/task/task-utils.js";

    function statusColor(status) {
        switch (status) {
            case 1:
                return "lightcoral";
            case 2:
                return "lightskyblue";
            case 3:
                return "lightgreen";
        }
    }

    onMount(() => {
        updateTasks()
        console.log(updateTasks())
    })
</script>

<div class="wrapper">
    {#if ($taskStore.length === 0) && ($groupStore.length === 0)}
        <p>No groups and tasks found. Please create some groups and tasks.</p>
    {:else if $taskStore.length === 0}
        <p>No tasks found. Please create some tasks.</p>
    {:else if $groupStore.length === 0}
        <p>No groups found. Please create some groups.</p>
    {:else}
        <table>
            <thead>
            <tr>
                <th>Group</th>
                {#each $taskStore as task}
                    <th>{task.taskname}</th>
                {/each}
            </tr>
            </thead>
            <tbody>
            {#each $groupStore as group}
                <tr>
                    <th>{group.name}</th>
                    {#await updateGroupTasks(group.name)}
                    {:then tasks}
                        {#each tasks as task}
                            <td>
                                <div class="task" style="background: {statusColor(task.status)}"/>
                            </td>
                        {/each}
                    {/await}
                </tr>
            {/each}
            </tbody>
        </table>
    {/if}
</div>

<!-- Table style copied from https://dev.to/dcodeyt/creating-beautiful-html-tables-with-css-428l-->
<style>
    .wrapper {
        box-sizing: border-box;
        border: 5px solid #009879;
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em;
        margin: 1em;
        width: max-content;
    }

    .task {
        padding: 5px;
        width: 10px;
        height: 10px;
        margin: auto 0;
    }

    table {
        border-collapse: collapse;
        margin: 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
    }

    table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }

    table th,
    table td {
        padding: 12px 15px;
    }

    table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }
</style>
