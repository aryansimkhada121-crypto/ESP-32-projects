from machine import PWM, Pin, I2C
import ssd1306
import time 

# OLED display Height and Width
OLED_WIDTH = 128
OLED_HEIGHT = 64

# initialize the rbg led pins
blue_pin = PWM(Pin(15), freq=1000)
green_pin = PWM(Pin(2), freq=1000)
red_pin = PWM(Pin(4), freq=1000)

#Initialize Oled display
i2c = I2C(0, sda = Pin(21), scl = Pin(22), freq=400000)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

#initalize the pir motion
motion_sensor = Pin(19, Pin.IN)

#initialize buzzer
buzzer = Pin(23, Pin.OUT)


#color function in (r,g,b) format 
def rgb_color(r, g, b):
    red_pin.duty_u16(int(r * 65535 / 255))
    green_pin.duty_u16(int(g * 65535 / 255))
    blue_pin.duty_u16(int(b * 65535 / 255))
    

#turn on the buzzer 
def buzzer_on():
    try:
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
    except KeyboardInterrupt:
        # Ensure the buzzer turns off when stopping the script
        buzzer.value(0)
        print("Program stopped.")

#check for motion
def motion_detect(sensor_state):
    
    #case: 1 (no motion)
    if sensor_state == 0:
        oled.fill(0)
        oled.text("Monitoring...", 0, 20)
        oled.show()
        rgb_color(0, 255, 0)
    #case: 2 (motion)
    elif sensor_state == 1:
        oled.fill(0)
        oled.text("Motion Detected!", 0, 20)
        oled.show()
        buzzer_on()
        rgb_color(255, 0, 0)
    #case: 3 (some error)
    else:
        oled.text("ERROR", 0, 20)
    

while True:
    state = motion_sensor.value()
    motion_detect(state)