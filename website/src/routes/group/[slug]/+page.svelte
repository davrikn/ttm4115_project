<script>
	import DeleteGroupButton from '$lib/group/DeleteGroupButton.svelte';
	import TaskViewer from '$lib/task/TaskViewer.svelte';
	import RequestHelpButton from '$lib/help/RequestHelpButton.svelte';

	export let data;
</script>

<div class="wrapper">
	<div class="bar">
		<h1>Group: {data.slug}</h1>
		<div class="buttons">
			<RequestHelpButton name={data.slug} />
			<DeleteGroupButton name={data.slug} />
		</div>
	</div>
	<TaskViewer groupname={data.slug} />
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
</style>
