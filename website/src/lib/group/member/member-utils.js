import {browser} from "$app/environment";
import {invalidateAll} from "$app/navigation";

export function addGroupmember(groupname, username) {
    if (username === undefined || username === null || username === "") {
        alert("Please enter a username");
        return;
    }
    if (browser) {
        fetch(`http://localhost:3000/groups/${groupname}/members`, {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
            },
            body: JSON.stringify({username: username})
        })
            .then((response) => response.text())
            .then((text) => {
                alert(text)
                invalidateAll()
            })
            .catch((err) => {
                alert(err);
            });
    }
}

export function removeGroupmember(groupname, username) {
    if (browser) {
        fetch(`http://localhost:3000/groups/${groupname}/members`, {
            method: 'DELETE', headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
            },
            body: JSON.stringify({username: username})
        })
            .then((response) => response.text())
            .then((text) => {
                alert(text)
            })
            .catch((err) => {
                alert(err);
            });
    }
}
