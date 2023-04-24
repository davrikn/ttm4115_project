<script>
let username;
let password;
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
            .then(response => {
                if (response.status === 200) {
                    window.location.href = '/';
                } else {
                    alert('Login failed');
                }
            })
            .catch(err => {
                alert('Login failed', err);
            });
}

</script>

<div class="form">
    <label>
        Username:
        <input bind:value={username} name="username" type="text">
    </label>
    <label>
        Password:
        <input bind:value={password} name="password" type="password">
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
