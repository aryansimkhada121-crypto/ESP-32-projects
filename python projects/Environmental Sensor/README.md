# ESP32 Smart Plant Monitor & Cloud IoT System

A modular, IoT-enabled plant monitoring system built with MicroPython, an ESP32, local sensors, Adafruit IO cloud synchronization, and a desktop Python analytics pipeline.

## Features

* **Local Display:** Real-time sensor metrics (soil moisture, temperature, humidity, light voltage) rendered locally on an ST7735 TFT screen every 0.5 seconds without display lag.
* **Cloud Sync:** Non-blocking background HTTP POST requests (`cloud.py`) pushing telemetry data to Adafruit IO every 30 seconds.
* **Desktop Analytics:** Python desktop script (`requests`, `pandas`, `matplotlib`) to pull historical cloud data, save it locally to a CSV (`plant_data.csv`), and generate trend graphs.

## Project Structure

* `main.py`: Core hardware loop, sensor polling, TFT screen updates, and sync timer logic.
* `cloud.py`: Modular wrapper class (`AdafruitIOCloud`) handling Adafruit IO REST API communication.
* `desktop_analytics.py`: Mac script for fetching historical feeds, local CSV logging, and plotting trends.

## Hardware Components

* ESP32 Development Board
* ST7735 TFT Display
* DHT11 Temperature & Humidity Sensor
* Soil Moisture Sensor
* LDR (Light Dependent Resistor) & Voltage Divider Circuit

## Troubleshooting & Known Errors

### 1. Hardware Short Circuit (VIN & GND Bridge)

* **The Error:** Accidental multimeter probe slip bridging the `VIN` and `GND` pins while an external power supply was active.
* **The Symptom:** The board shuts down instantly. Subsequent USB connections cause internal components (`U1` and `U2` voltage regulators) to heat up rapidly, failing to boot or enter the REPL.
* **The Fix:** The board's internal power management silicon was permanently damaged and required a hardware replacement. Always double-check multimeter probe placement and settings before measuring live power rails.

### 2. Wi-Fi Brownout / Reboot Loops

* **The Error:** The ESP32 crashes or reboots spontaneously the moment Wi-Fi connection is attempted.
* **The Cause:** High transient current draw spikes during Wi-Fi radio initialization pulling down the board's input voltage.
* **The Fix:** Added explicit transmit power capping in the initialization code (`wlan.config(txpower=8.5)`) to reduce peak current spikes during handshake.