# Potentiometer-Controlled Servo & RGB Dashboard

An interactive embedded systems project built for the ESP32 using MicroPython. This project reads real-time analog input from a potentiometer, translates it into precise angular data, and coordinates a servo motor, an RGB LED status indicator, and an SSD1306 OLED display.

## Features

* **Analog-to-Digital Conversion (ADC):** Reads live 16-bit values from a potentiometer.
* **Linear Mapping:** Proportionally translates raw sensor data into a 0–180 degree range.
* **Visual Feedback:**
* Displays the live calculated angle dynamically on an SSD1306 OLED screen.
* Changes the color of an RGB LED depending on the current angle threshold.


* **PWM Servo Control:** Generates a 50Hz Pulse Width Modulation (PWM) signal to drive an SG90 servo motor.

## Future Changes & Roadmap

* **External Power Supply Integration:** Further test and validate the servo motor under full operational load using an independent 5V power source (with a shared common ground) to bypass USB current limitations and prevent system brownouts.
* **Smoothing Filter:** Implement a moving average or deadzone filter in software to reduce jitter on the potentiometer readings.