<script>
    export let queue;

    import StopHelp from "$lib/help/StopHelp.svelte";
    import StartHelp from "$lib/help/StartHelp.svelte";
</script>

<div class="wrapper">
    <h1>Help queue</h1>
    {#await queue}
    {:then helpQueue}
        <div class="awaiting">
            <h2>Awaiting: </h2>
            <table>
                <tbody>
                {#each helpQueue.awaiting as group}
                    <tr>
                        <th>{group}</th>
                        <td>
                            <StartHelp groupname={group}/>
                        </td>
                    </tr>
                {/each}
                </tbody>
            </table>
        </div>
        <div class="receiving">
            <h2>Receiving: </h2>
            <table>
                <tbody>
            {#each helpQueue.receiving as group}
                <tr>
                    <th>{group}</th>
                    <td>
                <StopHelp groupname={group}/>
                    </td>
                </tr>
            {/each}
                </tbody>
            </table>
        </div>
    {:catch error}
        <p>{error.message}</p>
    {/await}
</div>

<style>
    .wrapper {
        box-sizing: border-box;
        width: max-content;
        border: 5px solid rgb(59, 174, 255);
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        margin: 1em;
    }
</style>
