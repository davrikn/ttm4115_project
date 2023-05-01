<script>
	export let name;
	export let tasks;
</script>

<div class="box">
	<a href="/group/{name}">
		<h3>Group: {name}</h3>
		<h4>Progress: Task </h4>
	</a>
</div>

<style>
	.box {
		box-sizing: border-box;
		width: max-content;
		border: 5px solid rgb(59, 174, 255);
		border-radius: 1em;
		box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
		padding: 1em 4em 1em 4em;
		margin: 1em;
	}
</style>
