<script>
    import NewGroup from '$lib/group/NewGroup.svelte';
    import StatusBar from '$lib/StatusBar.svelte';
    import HelpQueue from "$lib/help/HelpQueue.svelte";
    import AllGroups from "$lib/group/AllGroups.svelte";
</script>

<slot/>

<div class="wrapper">
    <NewGroup/>
    <AllGroups/>

    <StatusBar/>
    <HelpQueue/>
</div>

<style>
    .wrapper {
        margin: 1em;
    }
</style>
