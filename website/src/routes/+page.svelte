<script>
    import NewGroup from '$lib/NewGroup.svelte';
    import StatusBar from '$lib/StatusBar.svelte';
    import HelpQueue from "$lib/HelpQueue.svelte";
    import AllGroups from "$lib/AllGroups.svelte";
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
