# Smart Ambient Light Monitor

An ambient light sensing project built for the ESP32 using MicroPython. This project uses a Light Dependent Resistor (LDR) via an analog-to-digital converter (ADC) to continuously measure room lighting, categorizing the environment into specific tiers (bright, dim, or dark) and providing multi-modal feedback.

## Features

* **Ambient Light Sensing:** Reads live 16-bit analog data from an LDR circuit and calculates corresponding voltage levels.
* **Environmental Categorization:** Evaluates light thresholds (`medium` and `minx`) to classify ambient conditions dynamically.
* **Visual Status & Feedback:**
* Displays the current lighting state ("Room is bright", "Room is dim", "Room is dark") on an SSD1306 OLED screen.
* Coordinates an RGB LED to visually reflect the lighting tier (e.g., green for bright, yellow for dim, red for dark).


* **Serial Telemetry:** Outputs raw ADC and calculated voltage values to the console for debugging and monitoring.

## Future Changes & Roadmap

* **Automated Smart Home Integration (Scaling Up):** Expand the system into an automated lighting controller where environmental thresholds trigger real-world relays, such as turning on desk lamps or adjusting PWM-dimmed smart workspace lighting automatically based on ambient darkness.
* **Dynamic Threshold Calibration:** Implement a self-calibration routine during startup that samples the room's baseline lighting for a few seconds to automatically adjust the `medium` and `minx` values rather than using hardcoded constants.
* **Cloud Data Logging:** Send light level history over Wi-Fi to a web dashboard or home automation platform (like Home Assistant) to track daylight patterns throughout the day.