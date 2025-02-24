from flask import Flask, jsonify, request
from mqtt_listener import start_mqtt, discovered_devices, publish_discovery

app = Flask(__name__)

# Get all discovered devices
@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(list(discovered_devices.values()))

# Add a device to Home Assistant
@app.route('/add_device', methods=['POST'])
def add_device():
    data = request.json
    device_id = data.get('id')

    if device_id not in discovered_devices:
        return jsonify({"error": "Device not found"}), 404

    device_info = discovered_devices[device_id]
    publish_discovery(device_info)
    
    return jsonify({"message": "Device added to Home Assistant", "device": device_info})

if __name__ == '__main__':
    start_mqtt()
    app.run(host='0.0.0.0', port=5000)
