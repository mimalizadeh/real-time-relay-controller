# ESP32 Real-Time Controller - Firmware (v0.1)

This firmware is designed to control a 4-relay module using an ESP32 microcontroller. In version 0.1, the firmware solely focuses on receiving command data from the backend and toggling the physical state of the relays.

The codebase is highly modular and built upon the FreeRTOS operating system to ensure non-blocking network communication.

## 🛠 Tools and Dependencies
* **Framework:** ESP-IDF (v6.0.2)
* **Programming Language:** C
* **Drivers & Components:** `esp_wifi`, `mqtt`, `esp_sntp`, `esp_driver_gpio`, `freertos`

## 🏗 Software Architecture
The code is structured based on the Separation of Concerns principle, divided into the following modules:
* `wifi_manager`: Manages network connections and automatic retries.
* `mqtt_manager`: Handles connection to the MQTT broker and subscribes to command topics.
* `sntp_manager`: Synchronizes system time (NTP) for message validation and timestamping.
* `app_tasks`: Manages FreeRTOS tasks using `command_queue` for thread-safe command processing and execution.

## 🚀 Setup and Flashing

1. **Configuration:** Configure your network credentials (SSID, Password) and MQTT Broker URI using Kconfig:
   ```bash
   idf.py menuconfig
   ```
   Navigate to the project configuration menu to enter your Wi-Fi and MQTT parameters.

2. **Clean and Build:** Due to the modular architecture and CMake configuration, it is recommended to clean the cache before compiling:
   ```bash
   idf.py fullclean
   idf.py build
   ```

3. **Flash to ESP32:**
   ```bash
   idf.py -p /dev/ttyUSB0 flash monitor
   ```
   *(Adjust the serial port based on your operating system).*

## 📌 Development Status (v0.1)

- [x] Stable connection to Wi-Fi and MQTT Broker.
- [x] Listen to command topics (`devices/{device_id}/commands/relay/{relay_id}/set`).
- [x] Toggle GPIO pins connected to relays (ON/OFF).
- [ ] Save relay states in Non-Volatile Storage (NVS) for power-loss recovery (Planned for next version).