A digital climate-monitoring project built for the ESP32 using MicroPython. This script interfaces with a DHT11 sensor to capture live temperature and humidity data, presenting the climate metrics on an SSD1306 OLED screen while using an RGB status indicator to show comfort tiers.

Features
Environmental Sensing: Polls a DHT11 sensor to acquire real-time temperature (Celsius) and humidity (percentage) data.

Visual Climate Metrics: Formats and displays live temperature and humidity readings clearly on an SSD1306 OLED display.

Temperature Threshold Indicator: Coordinates an RGB LED to reflect ambient comfort zones (e.g., red for warm/hot conditions, sky blue for cool conditions, and green for a balanced comfort range).

Safe Initialization: Sets a default off-state for the RGB LED on startup before entering the active polling loop.

Future Changes & Roadmap
Smart HVAC & Fan Automation (Scaling Up): Expand the system by replacing or complementing the RGB indicator with real hardware actuators—such as triggering a relay-controlled DC fan when temperatures exceed a specific threshold or activating a humidifier based on low humidity levels.

Dual-Metric Threshold Logic: Enhance the conditional checking function (check_status) to factor in both temperature and humidity simultaneously (creating a heat index or comfort index) rather than relying solely on temperature.