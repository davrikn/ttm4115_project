<script>
    export let groupname;

    async function requestHelp() {
        if (groupname === undefined || groupname === null || groupname === "") {
            alert("Please enter a groupname");
            return;
        }
        await fetch('http://localhost:3000/help/request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
            },
            body: JSON.stringify({
                'groupname': groupname,
            })
        })
            .then((response) => response.text())
            .then((text) => {
                alert(text)
            })
            .catch((err) => {
                alert(err);
            });
    }
</script>

<button on:click={requestHelp}>Request help</button>

<style>
	button {
		background-color: darkblue; /* Green */
		border: black 2px solid;
		border-radius: 5px;
		color: white;
		padding: 15px 32px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		font-size: 16px;
		margin: 4px 2px;
		cursor: pointer;
	}
</style>
