<script>
    import NewGroup from '$lib/group/NewGroup.svelte';
    import AllGroups from "$lib/group/AllGroups.svelte";
    import StatusBar from "$lib/StatusBar.svelte";
</script>

<slot/>

<div class="wrapper">
    <NewGroup/>
    <AllGroups/>

    <StatusBar/>
</div>

<style>
    .wrapper {
        margin: 1em;
    }
</style>
