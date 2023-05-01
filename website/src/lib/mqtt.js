import mqtt_client from 'u8-mqtt'
import {browser} from "$app/environment";
import {invalidateAll} from "$app/navigation";
import {updateGroups} from "$lib/group/group-utils.js";
import {updateTasks} from "$lib/task/task-utils.js";


export async function run() {
    if (browser) {
        let my_mqtt = mqtt_client()
            .with_websock('ws://wirelogger.com:8080')
            .with_autoreconnect()

        await my_mqtt.connect()

        my_mqtt.subscribe_topic(
            'groups/*/status',
            (pkt, params, ctx) => {
                console.log('Group status')
                updateGroups()
                updateTasks()
            })

        my_mqtt.subscribe_topic(
            'help/status',
            (pkt, params, ctx) => {
                console.log('help status')
                invalidateAll()
            })

        my_mqtt.subscribe_topic(
            'groupCreated',
            (pkt, params, ctx) => {
                console.log('groupCreated')
                updateGroups()
            })

        my_mqtt.subscribe_topic(
            'groupCreated',
            (pkt, params, ctx) => {
                console.log('groupCreated')
                updateGroups()
            })
    }
}
