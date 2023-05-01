<script>
    import Group from '$lib/group/Group.svelte';
    import {updateGroups} from "$lib/group/group-utils.js";
    import {groupStore} from "$lib/stores.js";
    import {onMount} from "svelte";

    onMount(async () => updateGroups())
</script>

<div class="groups">
    {#each $groupStore as group}
        <Group groupname={group.name} tasks={group.tasks}/>
        {:else}
        <h1>There is no groups on the server.<br>
            Please create new groups.</h1>
    {/each}
</div>

<style>
    .groups {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
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
