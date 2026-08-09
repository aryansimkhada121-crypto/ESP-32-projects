from machine import Pin, PWM, I2C, ADC
import ssd1306
import time

# OLED display Height and Width
OLED_WIDTH = 128
OLED_HEIGHT = 64

#initalize the Potentiometer
pto = ADC(Pin(13))

#initalize the servo
sg90 = PWM(Pin(23), freq = 50)

#Initialize Oled display
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq=400000)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# initialize the rbg led pins
blue_pin = PWM(Pin(15), freq=1000)
green_pin = PWM(Pin(2), freq=1000)
red_pin = PWM(Pin(4), freq=1000)

#color function in (r,g,b) format 
def rgb_color(r, g, b):
    red_pin.duty_u16(int(r * 65535 / 255))
    green_pin.duty_u16(int(g * 65535 / 255))
    blue_pin.duty_u16(int(b * 65535 / 255))
    
# set the angle for the servo
def set_servo_angle(angle):
    
    percentage = angle/180
    
    duty = int((percentage * 3277) +3277)
    
    sg90.duty_u16(duty)

#color based on angle
def set_color_angle(angle):
    if 0 <= angle <= 90:
        rgb_color(255, 192, 203)
    elif 90 <= angle <= 130:
        rgb_color(127, 0, 255)
    elif angle >= 130:
        rgb_color(255, 215, 0)
    else:
        print("error")


while True:
    oled.fill(0)
    digital_value = pto.read_u16()
    
    ratio_to_deg = 180*(digital_value/65535)
    #set_servo_angle(ratio_to_deg)
    set_color_angle(ratio_to_deg)
    angle_display = str(180*(digital_value/65535))
    oled.text(angle_display, 0, 20)
    oled.show()
    time.sleep(0.1)
    