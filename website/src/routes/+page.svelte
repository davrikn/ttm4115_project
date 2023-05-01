<script>
    import NewGroup from '$lib/group/NewGroup.svelte';
    import AllGroups from "$lib/group/AllGroups.svelte";
    import StatusBar from "$lib/StatusBar.svelte";
</script>

<slot/>

<div class="wrapper">
    <div class="row"><NewGroup/> <StatusBar/>
    </div>
    <div class="groups">
    <AllGroups/>
    </div>
</div>

<style>
    .wrapper {
    }
    .row {
        display: flex;
        flex-direction: row;
        justify-content: center;

    }

    .groups {
        width: 100%;
        margin: 0;
        padding: 2em !important;
        display: flex;
        flex-direction: row;
        justify-content: center;
    }
</style>
