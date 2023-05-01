<script>
    import RemoveMember from "$lib/group/member/RemoveMember.svelte";

    export let groupname;
    export let groupmembers;
</script>

<div class="wrapper">
    <h3>Members:</h3>
    <table>
        <tbody>
        {#each groupmembers as member}
            <tr>
                <td>{member.username}</td>
                <td>
                    <RemoveMember groupname={groupname} username={member.username}/>
                </td>
        {/each}
        </tbody>
    </table>
</div>

<style>
    .wrapper {
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
</style>
