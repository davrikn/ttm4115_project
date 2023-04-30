<script>
    let groupname;
    function createNewGroup() {
        if (groupname === undefined || groupname === null || groupname === "") {
            alert("Please enter a group name");
            return;
        }
        fetch('http://localhost:3000/groups', {
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
            .then((text) => alert(text))
            .catch((err) => {
                alert(err);
            });
    }
</script>

<form>
<label for="new-group">
    New group name:
</label>
<input bind:value={groupname} type="text" name="new-group" id="new-group">
<button on:click={createNewGroup}>Create new group</button>
</form>

<style>

    form {
        box-sizing: border-box;
        width: max-content;
        border: 5px solid darkgreen;
        border-radius: 1em;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
        padding: 1em 4em 1em 4em;
        margin: 1em;

        display: flex;
        flex-direction: column;
        justify-content: space-between;
        justify-items: center;
        gap: 1em;
        align-items: flex-start;
    }
	button {
		background-color: darkgreen; /* Green */
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
