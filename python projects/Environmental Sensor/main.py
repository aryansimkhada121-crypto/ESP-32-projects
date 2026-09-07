from machine import PWM, Pin, SPI, ADC
import time
import dht
import st7735 as st7735
import sysfont as sysfont
import network
from cloud import Cloud

led = Pin(2, Pin.OUT)

class ADC_SENSOR:

    def __init__(self, pin_num, name="Sensor"):
        self.name = name
        self.adc = ADC(Pin(pin_num))
        self.adc.atten(ADC.ATTN_11DB)
        
    def read_voltage(self):
        digital_value = self.adc.read_u16()
        voltage = 3.3*(digital_value/65535)
        raw_percentage = 100*(digital_value/65535)
        percentage = 100 - raw_percentage

        print(f"[{self.name}]  ADC Value: {digital_value} |  Voltage: {voltage}V | Percentage: {percentage}%")
        return voltage, percentage, digital_value

class TemperatureClassifier:

    def __init__(self, low_limit = 15, high_limit = 30):
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.current_state = "UNKNOWN"

    def check_temp(self,current_temp):
        if current_temp <= self.low_limit:
            self.current_state = "COLD"
        elif self.low_limit <= current_temp <= self.high_limit:
            self.current_state = "IDEAL"
        else:
            self.current_state = "HOT"

class MoistureClassifier:

    def __init__(self, low_limit = 20, high_limit = 65):
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.current_state = "UNKNOWN"

    def check_moisture(self, current_moisture):
        if current_moisture <= self.low_limit:
            self.current_state = "DRY"
        elif self.low_limit <= current_moisture <= self.high_limit:
            self.current_state = "IDEAL"
        else:
            self.current_state = "WET"

class LightClassifier:

    def __init__(self, low_limit = 0.5, high_limit = 2.8):
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.current_state = "UNKNOWN"

    def check_voltage(self, current_voltage):
        if current_voltage <= self.low_limit:
            self.current_state = "DARK"
        elif self.low_limit <= current_voltage <= self.high_limit:
            self.current_state = "IDEAL"
        else:
            self.current_state = "SCORCHING"

class HumidityClassifier:

    def __init__(self, low_limit = 35, high_limit = 70):
        self.low_limit = low_limit
        self.high_limit = high_limit
        self.current_state = "UNKNOWN"

    def check_humidity(self, current_humidity):
        if current_humidity <= self.low_limit:
            self.current_state = "LOW"
        elif self.low_limit <= current_humidity <= self.high_limit:
            self.current_state = "IDEAL"
        else:
            self.current_state = "HIGH"

class SystemController:

    def __init__(self, Temperature, Moisture, Light, Humidity, display, font):
        self.temp = Temperature
        self.moisture = Moisture
        self.light = Light
        self.humidity = Humidity
        self.tft = display
        self.font = font

    def control_loop(self):

        temp_state = self.temp.current_state
        moisture_state = self.moisture.current_state
        light_state = self.light.current_state
        humidity_state = self.humidity.current_state

        #multi warning check
        active_warnings = []

        #temp 
        if temp_state == "HOT":
            active_warnings.append("TEMP: TOO HOT")
        elif temp_state == "COLD":
            active_warnings.append("TEMP: TOO COLD")

        #moisture
        if moisture_state == "WET":
            active_warnings.append("SOIL: TOO WET")
        elif moisture_state == "DRY":
            active_warnings.append("SOIL: TOO DRY")

        #light
        if light_state == "SCORCHING":
            active_warnings.append("LIGHT: SCORCHING")

        #humidity
        if humidity_state == "HIGH":
            active_warnings.append("HUMIDITY: HIGH")
        elif humidity_state == "LOW":
            active_warnings.append("HUMIDITY: LOW")

        # Priority 1: Dry Soil + High Temp
        #If the plant is dry and scorching, regular watering is not enough; it requires urgent intervention.
        if moisture_state == "DRY" and temp_state == "HOT":
            print("URGENT WATERING") #Call for Action
            #self.tft.text((15, 115), "URGENT WATERING ", self.tft.color(255, 0, 0), self.font)
            active_warnings.append("URGENT WATERING")

        #Priority 2: High Humidity + Wet Soil 
        #High moisture levels paired with stationary high humidity creates an ideal breeding environment for fungi and root rot.
        if humidity_state == "HIGH" and moisture_state == "WET":
            print("MOLD RISK WARNING") #Call for Action
            #self.tft.text((15, 115), "MOLD RISK ALERT ", self.tft.color(255, 165, 0), self.font)
            active_warnings.append("MOLD RISK")

        #Priority 3: Low Light
        #Even if the soil and temperature are ideal, the plant is not receiving enough energy to process them.
        if light_state == "DARK":
            print("INSUFFICIENT Light") #Call for Action
            #self.tft.text((15, 115), "LOW LIGHT FLAG  ", self.tft.color(255, 255, 0), self.font)
            active_warnings.append("INSUFFICIENT Light")

        list_length = len(active_warnings)

        self.tft.fillrect((0, 115), (128, 45), self.tft.color(0, 0, 0))

        if list_length == 0:
            self.tft.text((15, 115), "ALL GOOD :)", self.tft.color(255, 255, 255), self.font)
        elif list_length > 0:
            start_y = 115
            for waring in active_warnings:
                self.tft.text((15, start_y), waring, self.tft.color(0,0,255), self.font)
                start_y = 15 + start_y
                print(waring)
        

# Initialize hardware SPI
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))

# Initialize the ST7735 display using positional arguments: (spi, DC, Reset, CS)
tft = st7735.TFT(spi, Pin(14), Pin(27), Pin(26))
tft.initr()
tft.rgb(True)

# Clear screen to black
tft.fill(tft.color(0, 0, 0))

#Initalize the ADC sensors
moisture_sensor = ADC_SENSOR(pin_num=32, name="moisture sensor")
ldr_sensor = ADC_SENSOR(pin_num=36, name ="LDR")

#Initalize the dht sensor
dht_sensor = dht.DHT11(Pin(13))

#Initialize cloud handler Adafruit IO credentials
cloud = Cloud(username="", aio_key="")
last_upload = 0
upload_rate = 30

#Initalize the classes
temp_manager = TemperatureClassifier()
moisture_manager = MoistureClassifier()
voltage_manager = LightClassifier()
humidity_manager = HumidityClassifier()

#Initialize the Master Controller
main_controller = SystemController(temp_manager, moisture_manager, voltage_manager, humidity_manager, tft, sysfont.sysfont)

#Initialize wifi 
def connect_wifi():
    tft.fillrect((5, 20), (120, 15), tft.color(0, 0, 0))
    tft.text((5, 20), "Connecting WiFi...", tft.color(255, 255, 0), sysfont.sysfont)
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Cap RF transmit power to prevent brownout spikes
    try:
        wlan.config(txpower=8.5)
    except Exception:
        pass
        
    time.sleep(1)
    wlan.connect('', '')
    
    timeout = 0
    while not wlan.isconnected() and timeout < 10:
        led.value(not led.value())
        time.sleep(1)
        timeout += 1
        
    tft.fillrect((5, 20), (120, 15), tft.color(0, 0, 0))
    if wlan.isconnected():
        tft.text((5, 20), "WiFi: OK!", tft.color(0, 255, 0), sysfont.sysfont)
    else:
        tft.text((5, 20), "WiFi: TIMEOUT", tft.color(255, 0, 0), sysfont.sysfont)

#start the wifi
connect_wifi()
time.sleep(1)

try:
    tft.fill(tft.color(0, 0, 0))
    tft.text((5, 10), "ENVIRONMENTAL SENSOR", tft.color(255, 255, 255), sysfont.sysfont)
    while True:
        #call the function and both returned values
        ldr_voltage, _, _x = ldr_sensor.read_voltage()
        voltage_manager.check_voltage(ldr_voltage)

        _, moisture_percentage, _y = moisture_sensor.read_voltage()
        moisture_manager.check_moisture(moisture_percentage)
        
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            temp_manager.check_temp(temp)
            humi = dht_sensor.humidity()
            humidity_manager.check_humidity(humi)
        except Exception:
            pass

        volt = f"Voltage: {ldr_voltage:.2f} V "
        tft.text((15, 50), volt, tft.color(255, 0, 0), sysfont.sysfont)

        moisture = f"Moisture: {moisture_percentage:.2f} % "
        tft.text((15, 65), moisture, tft.color(25, 200, 120), sysfont.sysfont)

        temperature = f"Temp: {temp} C"
        tft.text((15, 80), temperature, tft.color(0, 200, 3), sysfont.sysfont)

        humidity = f"Humidity: {humi} %"
        tft.text((15, 95), humidity, tft.color(0, 200, 3), sysfont.sysfont)

        main_controller.control_loop()

        current_time = time.time()

        if current_time - last_upload >= upload_rate:
            cloud.send_all(moisture_percentage, temp, humi, ldr_voltage)
            last_upload = current_time

        time.sleep(0.5)
        print("\n")

except KeyboardInterrupt:
    print("\nProgram stopped no erorrs.")