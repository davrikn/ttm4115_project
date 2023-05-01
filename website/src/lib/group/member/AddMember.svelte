<script>
    import {addGroupmember} from "$lib/group/member/member-utils.js";

    export let groupname;
    let username;
</script>

<form>
    <label for="username">
        Add user to group:
    </label>
    <input bind:value={username} type="text" name="username" id="username">
    <button on:click={() => addGroupmember(groupname, username)}>Add user</button>
</form>

<style>
    form {
        box-sizing: border-box;
        width: max-content;
        border: 5px solid darkgreen;
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        height: 100%;

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
