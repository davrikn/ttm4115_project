import mqtt_client from 'u8-mqtt'
import {browser} from "$app/environment";


export async function run() {
    if (browser) {
        let my_mqtt = mqtt_client()
            .with_websock('ws://wirelogger.com:8080')
            .with_autoreconnect()

        await my_mqtt.connect()

        my_mqtt.subscribe_topic(
            'group/*/status',
            (pkt, params, ctx) => {
                console.log('topic packet', params, pkt, pkt.json())
            })

        await my_mqtt.json_send(
            'group/group1/status',
            { note: 'from README example',
                live: new Date().toISOString() })
    }
}
