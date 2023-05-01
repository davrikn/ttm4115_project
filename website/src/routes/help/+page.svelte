<script>
export let data;
import HelpQueue from "$lib/help/HelpQueue.svelte";
</script>

<slot/>
<div>
    <HelpQueue queue={data.queue}/>
</div>


<style>
div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}
</style>
