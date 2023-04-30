<script>
import {updateGroups} from "$lib/group/group-utils.js";

let taskname;
async function createNewTask() {
    if (taskname === undefined || taskname === null || taskname === "") {
        alert("Please enter a taskname");
        return;
    }
    await fetch('http://localhost:3000/groups', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
        },
        body: JSON.stringify({
            'taskname': taskname,
        })
    })
        .then((response) => response.text())
        .then((text) => {
            alert(text)
            updateGroups()
        })
        .catch((err) => {
            alert(err);
        });
}
</script>

<form>
    <label for="new-task">
        New task name:
    </label>
    <input bind:value={taskname} type="text" name="new-task" id="new-task">
    <button on:click={createNewTask}>Create new task</button>
</form>

<style>
    form {
        box-sizing: border-box;
        width: max-content;
        border: 5px solid darkgreen;
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        margin: 1em;

        display: flex;
        flex-direction: column;
        justify-content: space-between;
        justify-items: center;
        gap: 1em;
        align-items: flex-start;
    }
    button {
        background-color: darkgreen; /* Green */
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
