<script>
export let data;
import HelpQueue from "$lib/help/HelpQueue.svelte";
</script>

<slot/>
<HelpQueue queue={data.queue}/>

<style>

</style>
