# ESP32 Radar Warning Receiver (RWR) Proximity System

An embedded MicroPython-based proximity sensing and threat alert system designed to replicate military-style **Radar Warning Receiver (RWR)** behaviors. It utilizes live distance tracking to dynamically shift visual interfaces, physical RGB indicator states, and audio warning patterns.

---

## Features

* **Real-Time Distance Tracking:** Measures target proximity via an HC-SR04 ultrasonic sensor.
* **Dynamic TFT Display UI:** Renders live telemetry data, custom headers, and multi-state threat warnings on a 1.8" ST7735 color display.
* **Tiered Threat Response System:**
* **Scanning State ($\ge$ 50 cm):** Dim green indicator and slow sonar pulses.
* **Lock/Warning State (35–50 cm):** Golden/orange lighting, rapid locking tones, and hazard prompts.
* **Critical Threat State ($<$ 35 cm):** Flashing red indication, high-frequency stutter warnings, and collision alerts.


* **Safe Resource Management:** Implements robust exception and cleanup loops to safely power down PWM pins and clear states upon interruption.

---

## Hardware Components

* **Microcontroller:** ESP32 Wi-Fi/BLE Module
* **Display:** 1.8" TFT LCD (128x160 resolution, ST7735 driver)
* **Sensor:** HC-SR04 Ultrasonic Distance Sensor
* **Visual Output:** Common Anode/Cathode RGB LED
* **Audio Output:** Passive Buzzer driven via an **NPN 2222A transistor**
* **Resistors:**
* $3 \times 220\,\Omega$ resistors (for RGB LED current limiting)
* $1 \times 1\,\text{k}\Omega$ resistor (for transistor base current limiting)



---

## Future Improvements

* **Enhanced Audio Engine:** Integration of a **DFPlayer Mini** audio module alongside the passive buzzer to play high-fidelity, authentic RWR threat sample sounds for absolute realism.