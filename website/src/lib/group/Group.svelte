<script>
    export let groupname;
    export let tasks;
    const taskLength = () => Object.keys(tasks).length
    const getDoneTasks = () => Object
        .values(tasks)
        .filter(status => status === 3)
        .length
</script>

<div class="box">
    <a href="/group/{groupname}">
        <h3>Group: {groupname}</h3>
        <h4>Done with <br/> {getDoneTasks()} tasks of {taskLength()} </h4>
        <p>Click widget to see more</p>
    </a>
</div>

<style>
    .box {
        box-sizing: border-box;
        width: max-content;
        border: 5px solid rgb(59, 174, 255);
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        margin: 1em;
    }
</style>
