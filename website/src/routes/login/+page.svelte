<script>
	import jwt_token from '$lib/token.js';
	import { goto } from '$app/navigation';
	let username;
	let password;
	$: loggedIn = false;
	function login() {
		fetch('http://localhost:3000/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username,
				password
			})
		})
			.then((response) => {
				if (response.ok) return response.json();
				else throw Error('Wrong username or password!');
			})
			.then((data) => {
				if (data.access_token) {
					jwt_token.set(data.access_token);
					// headers: {
					//     Authorization: `Bearer ${localStorage.getItem("jwt_token")}`
					// },
					goto('/');
				}
			})
			.catch((err) => {
				alert(err);
			});
	}
</script>

<div class="form">
	<label>
		Username:
		<input bind:value={username} name="username" type="text" />
	</label>
	<label>
		Password:
		<input bind:value={password} name="password" type="password" />
	</label>
	<button on:click={login}>Log in</button>
</div>

<style>
	.form {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex-wrap: wrap;
	}

	button {
		margin: 1em;
		width: 5em;
	}

	label {
		margin: 1em;
	}
</style>
