<script>
	import TaskViewer from '$lib/task/TaskViewer.svelte';
	import RequestHelpButton from '$lib/help/RequestHelpButton.svelte';
	import Members from "$lib/group/member/Members.svelte";

	export let data;
</script>

<div class="wrapper">
	<div class="bar">
		<h1>Group: {data.slug}</h1>
		<div class="buttons">
			<RequestHelpButton name={data.slug} />
		</div>
	</div>
	<Members groupname={data.slug} groupmembers={data.groupmembers}/>
	<TaskViewer tasks={data.tasks} groupname={data.slug} />
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
