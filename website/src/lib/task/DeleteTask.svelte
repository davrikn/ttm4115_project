<script>
    import {updateTasks} from "$lib/task/task-utils.js";

    export let taskname;

    async function deleteTask() {
        if (taskname === undefined || taskname === null || taskname === "") {
            alert("Please enter a taskname");
            return;
        }
        await fetch(`http://localhost:3000/tasks/${taskname}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
            },
        })
            .then((response) => response.text())
            .then((text) => {
                alert(text)
                updateTasks()
            })
            .catch((err) => {
                alert(err);
            });
    }
</script>


<button on:click={deleteTask}>Delete task</button>

<style>
    button {
        background-color: darkred; /* Green */
        border: black 2px solid;
        border-radius: 5px;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
</style>
