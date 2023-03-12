<script>
    import Button from "../lib/Button.svelte";

    const c1 = () => console.log("un")
    const c2 = () => console.log("dos")
    const c3 = () => console.log("tres")
</script>

<div class="w-6/12 flex flex-col align-center self-center border-r-2 border-l-2 border-b-2 border-black bg-emerald-300">
    <p class="text-center mb-2.5">Worlds' best app</p>
    <div class="flex flex-row justify-center mb-1">
        <Button click={c1} buttonText="En knapp"/>
        <Button click={c2} buttonText="To knapp"/>
        <Button click={c3} buttonText="Tre knapp"/>
    </div>
</div>