<script>
	import Group from '$lib/Group.svelte';
	import NewGroupButton from '$lib/NewGroupButton.svelte';
	import NavBar from '$lib/NavBar.svelte';
	import StatusBar from '$lib/StatusBar.svelte';
</script>

<NavBar />
<div class="wrapper">
	<div class="buttons-row">
		<NewGroupButton />
	</div>
	<div class="groups">
		<Group name="1" tasks="[1,2,3]" />
		<Group name="Test" tasks="[1,2,3]" />
		<Group name="6" tasks="[1,2,3]" />
	</div>

	<StatusBar />
</div>

<style>
	.wrapper {
		margin: 1em;
	}
	.buttons-row {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		padding: 0 1rem;
	}

	.groups {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		flex-wrap: wrap;
	}

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
