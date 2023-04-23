<script>
	import DeleteGroupButton from '$lib/DeleteGroupButton.svelte';
	import TaskViewer from '$lib/TaskViewer.svelte';
	import NavBar from '$lib/NavBar.svelte';
	import RequestHelpButton from '$lib/RequestHelpButton.svelte';

	export let data;
</script>

<NavBar />
<div class="wrapper">
	<div class="bar">
		<h1>Group: {data.slug}</h1>
		<div class="buttons">
			<RequestHelpButton name={data.slug} />
			<DeleteGroupButton name={data.slug} />
		</div>
	</div>
	<TaskViewer name="1" />
</div>

<style>
	.bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.wrapper {
		padding: 2rem 5rem;
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
