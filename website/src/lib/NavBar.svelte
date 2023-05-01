<script>
	import { browser } from '$app/environment';
	import jwt_token from '$lib/token.js';

	function logout() {
		if (browser) {
			localStorage.clear();
			jwt_token.set(undefined);
		}
	}
</script>

<nav>
	<a href="/">Home</a>
	<a href="/tasks">Tasks</a>
	<a href="/help">Help Queue</a>
	{#if !$jwt_token}
		<a href="/login">Login</a>
	{:else}
		<a on:click={logout}>Logout</a>
	{/if}
</nav>

<style>
	nav {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 0 1rem;
		background-color: #333;
		color: #fff;
	}
	nav a {
		color: #fff;
		text-decoration: none;
		padding: 0.5rem 1rem;
	}
	nav a:hover {
		background-color: #555;
	}
</style>
