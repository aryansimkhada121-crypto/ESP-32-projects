# PIR Motion Detection Security Node

An embedded security and monitoring script built for the ESP32 using MicroPython. This project uses a Passive Infrared (PIR) motion sensor to detect movement, providing immediate multi-modal feedback via an RGB status indicator, an active buzzer alert, and live status updates on an SSD1306 OLED display.

## Features

* **PIR Motion Monitoring:** Continuously polls a digital input pin to detect physical movement within the sensor's range.
* **Visual Status & Alerts:**
* Displays system states ("Monitoring..." vs. "Motion Detected!") dynamically on an SSD1306 OLED screen.
* Uses an RGB LED as a status indicator (Green for safe monitoring, Red for triggered alerts).


* **Audible Warning:** Triggers a pulsed buzzer alert immediately upon detecting motion.
* **Safe State Handling:** Includes exception catching to ensure hardware (like the buzzer) resets safely if interrupted.

## Future Changes & Roadmap

* **Network & IoT Scaling:** Integrate Wi-Fi capability to transmit motion event alerts and security logs to a remote dashboard or messaging service (such as MQTT or Telegram) for remote monitoring.
* **Armed/Disarmed State Machine:** Add a physical button or keypad interface to toggle the security node between armed and disarmed states, preventing false triggers during routine movement.
* **Event Logging:** Implement a timestamped local history log displayed on a larger OLED view or saved to flash storage.