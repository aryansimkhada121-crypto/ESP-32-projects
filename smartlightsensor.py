from machine import PWM, Pin, I2C, ADC
import ssd1306
import utime

medium = 25000
minx = 20000

#initalize the LDR 
ldr = ADC(Pin(4))

# OLED display Height and Width
OLED_WIDTH = 128
OLED_HEIGHT = 64

#Initialize Oled display
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq=400000)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# initialize the rbg led pins
blue_pin = PWM(Pin(15), freq=1000)
green_pin = PWM(Pin(18), freq=1000)
red_pin = PWM(Pin(2), freq=1000)

#color function in (r,g,b) format 
def rgb_color(r, g, b):
    red_pin.duty_u16(int(r * 65535 / 255))
    green_pin.duty_u16(int(g * 65535 / 255))
    blue_pin.duty_u16(int(b * 65535 / 255))
    

#check light levels
def light_level(light):
    # room is bright
    if light > medium:
        oled.fill(0)
        oled.text("Room is bright", 0, 20)
        oled.show()
        rgb_color(0, 255, 0)
    #room is dim
    elif minx < light < medium:
        oled.fill(0)
        oled.text("Room is dim", 0, 20)
        oled.show()
        rgb_color(255, 255, 0)
    #room is dark
    elif light < minx:
        oled.fill(0)
        oled.text("Room is dark", 0, 20)
        oled.show()
        rgb_color(255, 0, 0)
    else:
        print("error")

while True:
    digital_value = ldr.read_u16()
    print("ADC value=",digital_value)
    volt=3.3*(digital_value/65535)
    print("Voltage: {}V ".format(volt))
    light_level(digital_value)
    utime.sleep(1)
    