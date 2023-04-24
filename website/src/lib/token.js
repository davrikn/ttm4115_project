import {writable} from "svelte/store";
import {browser} from "$app/environment";

let initalValue = browser ? localStorage.getItem("jwt_token") : undefined

let jwt_token = writable(initalValue)

jwt_token.subscribe(token => {
    if (browser && token) {
        localStorage.setItem("jwt_token", token)
    }
})

export default jwt_token
