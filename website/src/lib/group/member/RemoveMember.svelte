<script>
    import {removeGroupmember} from "$lib/group/member/member-utils.js";

    export let groupname;
    export let username;
</script>


<button on:click={() => removeGroupmember(groupname, username)}>Remove {username}</button>

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
