<script>
    import DeleteTask from "$lib/task/DeleteTask.svelte";

    export let task;
</script>

<div>
    <p><strong>Task {task.taskname}</strong>: {task.task}</p>
    <DeleteTask taskname={task.taskname} />
</div>

<style>
    div {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 2em;

        box-sizing: border-box;
        width: max-content;
        border: 5px solid rgb(59, 174, 255);
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        max-width: 70%;
    }

    p {
        word-break: break-word;
    }
</style>
