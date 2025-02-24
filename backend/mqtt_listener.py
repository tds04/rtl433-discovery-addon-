import paho.mqtt.client as mqtt
import json
import os

MQTT_BROKER = os.getenv('MQTT_BROKER', 'homeassistant.local')
MQTT_PORT = 1883
MQTT_TOPIC = 'rtl_433/#'

discovered_devices = {}

# Handle incoming MQTT messages
def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    device_id = payload.get('id', message.topic)

    discovered_devices[device_id] = payload
    print(f"Discovered device: {device_id}")

# Publish MQTT discovery payload
def publish_discovery(device_info):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    
    discovery_topic = f"homeassistant/sensor/{device_info['id']}/config"
    discovery_payload = {
        "name": device_info.get("name", f"rtl433_{device_info['id']}"),
        "state_topic": f"rtl_433/{device_info['id']}",
        "unique_id": device_info['id'],
        "device": {
            "identifiers": [device_info['id']],
            "name": device_info.get("name", "RTL433 Device")
        }
    }
    
    client.publish(discovery_topic, json.dumps(discovery_payload), retain=True)
    client.disconnect()

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()
