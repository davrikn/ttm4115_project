<!-- Heavily inspired from https://svelte.dev/repl/b225504c9fea44b189ed5bfb566df6e6?version=3.58.0-->
<script>
	// Inspired by https://svelte.dev/repl/810b0f1e16ac4bbd8af8ba25d5e0deff?version=3.4.2.
	import { flip } from 'svelte/animate';
	export let tasks;

	let categories = [
		{
			name: 'NOT STARTED',
			items: ['task1', 'task2', 'task3']
		},
		{
			name: 'IN PROGRESS',
			items: ['task4']
		},
		{
			name: 'DONE',
			items: ['task5']
		}
	];

	for (let category in categories) {
		for (let task in tasks) {
			if (task.status === category.name) {
				category.items.push(task);
			}
		}
	}

	let hoveringOverBasket;

	function dragStart(event, basketIndex, itemIndex) {
		// The data we want to make available when the element is dropped
		// is the index of the item being dragged and
		// the index of the basket from which it is leaving.
		const data = { basketIndex, itemIndex };
		event.dataTransfer.setData('text/plain', JSON.stringify(data));
	}

	function drop(event, basketIndex) {
		event.preventDefault();
		const json = event.dataTransfer.getData('text/plain');
		const data = JSON.parse(json);

		// Remove the item from one basket.
		// Splice returns an array of the deleted elements, just one in this case.
		const [item] = categories[data.basketIndex].items.splice(data.itemIndex, 1);

		// Add the item to the drop target basket.
		categories[basketIndex].items.push(item);
		categories = categories;

		hoveringOverBasket = null;
	}
</script>

<p>Drag and drop tasks</p>

{#each categories as category, categoryIndex (category)}
	<div animate:flip>
		<b>{category.name}</b>
		<ul
			class:hovering={hoveringOverBasket === category.name}
			on:dragenter={() => (hoveringOverBasket = category.name)}
			on:dragleave={() => (hoveringOverBasket = null)}
			on:drop={(event) => drop(event, categoryIndex)}
			ondragover="return false"
		>
			{#each category.items as item, itemIndex (item)}
				<div class="item" animate:flip>
					<li draggable={true} on:dragstart={(event) => dragStart(event, categoryIndex, itemIndex)}>
						{item}
					</li>
				</div>
			{/each}
		</ul>
	</div>
{/each}

<style>
	.hovering {
		border-color: orange;
	}
	.item {
		display: inline; /* required for flip to work */
	}
	li {
		background-color: lightgray;
		cursor: pointer;
		display: inline-block;
		margin-right: 10px;
		padding: 10px;
	}
	li:hover {
		background: orange;
		color: white;
	}
	ul {
		border: solid lightgray 1px;
		display: flex; /* required for drag & drop to work when .item display is inline */
		height: 40px; /* needed when empty */
		padding: 10px;
	}
</style>
