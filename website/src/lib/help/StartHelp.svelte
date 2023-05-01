<script>

    import {startHelp} from "$lib/help/help-utils.js";

    export let groupname;
</script>


<button on:click={() => startHelp(groupname)}>Start help</button>

<style>
    button {
        background-color: green; /* Green */
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
