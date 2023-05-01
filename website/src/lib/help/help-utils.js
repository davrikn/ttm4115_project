import {browser} from "$app/environment";
import {invalidateAll} from "$app/navigation";


export function startHelp(groupname) {
    if (browser) {
        fetch(`http://localhost:3000/help/start`, {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
            },
            body: JSON.stringify({groupname: groupname})
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

export function stopHelp(groupname) {
    if (browser) {
        fetch(`http://localhost:3000/help/finish`, {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("jwt_token")}`
            },
            body: JSON.stringify({groupname: groupname})
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
