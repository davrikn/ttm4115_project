<script>
    import Group from '$lib/group/Group.svelte';
    import {updateGroups} from "$lib/group/group-utils.js";
    import {groupStore} from "$lib/stores.js";
    import {onMount} from "svelte";

    onMount(async () => updateGroups())
</script>

<div class="groups">
    {#each $groupStore as group}
        <Group name={group.name} tasks={group.tasks}/>
    {/each}
</div>

<style>
    .groups {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
</style>
