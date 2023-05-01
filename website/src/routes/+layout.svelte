<script>
    import NavBar from "$lib/NavBar.svelte";
    import { run } from "$lib/mqtt.js"

    run()
</script>

<NavBar />
<slot />

<style>
    :global(html) {
        font-family: Arial, serif;
        padding: 0;
        margin: 0;
    }

    :global(body) {
        font-family: Arial, serif;
        padding: 0;
        margin: 0;
    }

    :global(a) {
        color: inherit;
        text-decoration: none;
    }
</style>
