<script>
    import Group from '$lib/Group.svelte';
</script>

    <div class="groups">
        <Group name="1" tasks="[1,2,3]"/>
        <Group name="Test" tasks="[1,2,3]"/>
        <Group name="6" tasks="[1,2,3]"/>
    </div>

<style>
    .groups {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
</style>
