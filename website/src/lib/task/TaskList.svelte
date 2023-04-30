<script>
    import {onMount} from "svelte";
    import {updateTasks} from "$lib/task/task-utils.js";
    import {taskStore} from "$lib/stores.js";
    import Task from "$lib/task/Task.svelte";

    onMount(async () => updateTasks());
</script>

<div class="tasks">
    {#each $taskStore as task}
        <Task task={task} />
    {:else}
        <h1>There is no tasks on the server.<br>
            Please create new tasks.</h1>
    {/each}
</div>

<style>
    h1 {
        box-sizing: border-box;
        width: max-content;
        border: 5px solid darkred;
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        margin: 1em;
    }
</style>
