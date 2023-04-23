<script>
	let groups = [
		{
			name: 'Group 1',
			tasks: ['lightgreen', 'lightgreen', 'lightcoral', 'lightcoral', 'lightcoral']
		},
		{
			name: 'Group 2',
			tasks: ['lightgreen', 'lightgreen', 'lightcoral', 'lightcoral', 'lightcoral']
		},
		{
			name: 'Group 3',
			tasks: ['lightgreen', 'lightcoral', 'lightgreen', 'lightcoral', 'lightcoral']
		},
		{
			name: 'Group 4',
			tasks: ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']
		},
		{
			name: 'Group 5',
			tasks: ['lightgreen', 'lightgreen', 'lightgreen', 'lightcoral', 'lightcoral']
		}
	];
</script>

<div class="wrapper">
	{#each groups as group}
		<div class="container">
			<p>{group.name}:</p>

			{#each group.tasks as task}
				<div class="task" style="background: {task}" />
			{/each}
		</div>
	{/each}
</div>

<style>
	.wrapper {
		box-sizing: border-box;
		border: 5px solid lightblue;
		border-radius: 1em;
		box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
		padding: 1em 4em 1em 4em;
		margin: 1em;
		width: max-content;
	}

	.task {
		/*border: 5px solid lightgreen;*/
		padding: 5px;
		width: 10px;
		height: 10px;
		margin: auto 0;
	}

	.container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: flex-start;
		gap: 10px;
	}
</style>
