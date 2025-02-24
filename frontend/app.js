const API_URL = '/api';

// Fetch discovered devices
async function fetchDevices() {
    const response = await fetch(`${API_URL}/devices`);
    const devices = await response.json();
    const list = document.getElementById('device-list');
    list.innerHTML = '';

    devices.forEach(device => {
        const item = document.createElement('li');
        item.innerHTML = `
            <input type="checkbox" id="${device.id}" />
            <label for="${device.id}">${device.name || 'Unknown Device'} (${device.id})</label>
            <button onclick="addDevice('${device.id}')">Add to Home Assistant</button>
        `;
        list.appendChild(item);
    });
}

// Add device to Home Assistant
async function addDevice(deviceId) {
    const response = await fetch(`${API_URL}/add_device`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: deviceId })
    });

    const result = await response.json();
    alert(result.message || 'Device added!');
}

// Fetch devices on page load
fetchDevices();
