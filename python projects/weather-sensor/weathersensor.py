from machine import Pin, PWM, I2C
import ssd1306
import dht 
import time


# initialize the rbg led pins
blue_pin = PWM(Pin(2), freq=1000)
green_pin = PWM(Pin(4), freq=1000)
red_pin = PWM(Pin(23), freq=1000)

#color function in (r,g,b) format 
def rgb_color(r, g, b):
    red_pin.duty_u16(int(r * 65535 / 255))
    green_pin.duty_u16(int(g * 65535 / 255))
    blue_pin.duty_u16(int(b * 65535 / 255))
    
#inital state
rgb_color(0,0,0)

#initialize OLED display for use
OLED_WIDTH = 128
OLED_HEIGHT = 64

i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq=400000)

oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

    

sensor_dht = dht.DHT11(Pin(18))


def check_status(temp):
    if temp > 25:
        rgb_color(255, 0, 0)
    elif temp < 22:
        rgb_color(135, 206, 235)
    else:
        rgb_color(0,255,0)
        
while True:
    sensor_dht.measure()
    
    temp = sensor_dht.temperature()
    hum = sensor_dht.humidity()
    
    check_status(temp)
    
    oled.fill(0)
    oled.text("Temp: {} C".format(temp), 0, 0)
    oled.text("Hum: {} %".format(hum), 0, 20)
    oled.show()
    
    time.sleep(1)
        

