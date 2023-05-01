<script>
    import CreateTask from "$lib/task/CreateTask.svelte";
    import TaskList from "$lib/task/TaskList.svelte";
</script>
<div>
    <CreateTask/>
    <TaskList/>
</div>
<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 2em;
        height: 100%;
    }
</style>
