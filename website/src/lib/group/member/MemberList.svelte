<script>
    export let groupmembers;
</script>

<div>
    <h4>Members:</h4>
    {#each groupmembers as member}
        <p>{member.username}</p>
    {/each}
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        margin: 0;
        height: 100%;

        box-sizing: border-box;
        width: max-content;
        border: 5px solid rgb(59, 174, 255);
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        max-width: 70%;
    }

    p {
        margin: 5px;
    }
</style>
