ESP32 Real-Time Controller - Backend (v0.1)
===========================================

This backend service is designed to send real-time commands to ESP32 hardware nodes.
In version 0.1, the system is kept very simple. It only focuses on sending commands to turn relays ON or OFF. Databases
and receiving status data from the ESP32 are planned for future versions.

Technology Stack
----------------

* Core Framework: FastAPI (Python)
* Messaging Protocol: MQTT using the aiomqtt library
* Infrastructure: Docker (for running the MQTT Broker)

MQTT Topic Structure
--------------------
Currently, the backend only sends commands to the board.

* Send Command: `devices/{device_id}/commands/relay/{relay_id}/set`

Quick Start Setup
-----------------

1. Start the MQTT Broker inside Docker.
2. Install Python dependencies:
    ``` bash
    pip install -r requirements.txt
   ```
3. Run the FastAPI server:
    ``` bash
    uvicorn main:app --host 0.0.0.0 --port 8000
   ```

Development Status (v0.1)
-------------------------

- [x] Connect to the MQTT Broker using FastAPI.
- [x] Send ON/OFF commands to the ESP32 hardware.
- [ ] Receive relay state data from ESP32 (Planned for next version).
- [ ] Add databases for saving logs and states (Planned for next version).
- [ ] Detect if the ESP32 is offline (LWT) (Planned for next version).
