from machine import Pin, SPI, PWM
import time
import utime
from hcsr04 import HCSR04
import st7735
import sysfont
import random

#initalize the sensor
ultra_sonic = HCSR04(trigger_pin = 13, echo_pin = 22)

#Initialize the buzzer pin (GPIO-33)
buzzer = PWM(Pin(33))

# Initialize hardware SPI
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

# Initialize the ST7735 display using positional arguments: (spi, DC, Reset, CS)
tft = st7735.TFT(spi, Pin(2), Pin(4), Pin(5))
tft.initr()
tft.rgb(True)

# Clear screen to black
tft.fill(tft.color(0, 0, 0))

# initialize the rbg led pins
blue_pin = PWM(Pin(26), freq=1000)
green_pin = PWM(Pin(14), freq=1000)
red_pin = PWM(Pin(27), freq=1000)

#color function in (r,g,b) format 
def rgb_color(r, g, b):
    red_pin.duty_u16(int(r * 65535 / 255))
    green_pin.duty_u16(int(g * 65535 / 255))
    blue_pin.duty_u16(int(b * 65535 / 255))


# sound function to generate sound 
def play_sound(freq, duration_ms):
    if freq <= 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(int(freq))
        buzzer.duty_u16(32768)
    time.sleep_ms(duration_ms)

# RWR-search,lock, and warning/launch (RADAR WARNING RECIVER) sounds (as realstic as it can be)
def rwr_search():
    #Slow tone (object is out of designated range)
    
    #print("RWR: Object Scanning...")
    for i in range(3):
        play_sound(1800, 50)
        play_sound(0, 450)
        
def rwr_lock():
    #Faster tone (object is in designated safe distance from sensor)
    #print(f"RWR: [WARNING] Target Locked at {distance}cm! Approach Stopped - Danger Threshold!!")
    
    for i in range(10):
        play_sound(2200, 100)
        play_sound(0, 100)

def rwr_warning():
    #very fast tone (object is very close imminent threat warning from RWR)
    #verrrry hyper-aggressive, chaotic tone to maximize the imminent threat incoming, trying to replicate real life threat in combats cases

    #print(f"RWR: [CRITICAL] COLLISION AT {distance}cm! IMPACT IMMINENT - REVERSE NOW!")
    
    for burst in range(4):
        
        for freq in range(2200, 1200, -80):
            play_sound(freq, 6)
    
        for stutter in range(8):
            play_sound(2400, 15)  
            play_sound(900, 10)
        
        buzzer.duty_u16(0)
        time.sleep_ms(30)
        

def detect_distance(object):
    #object is farther that 50 cm, play rwr_search()
    if object >= 50:
        rgb_color(0, 150, 0) #dim green
        print(f"RWR: Object Scanning... Distance:{object}")
        tft.text((15, 75), "RWR: SCANNING", tft.color(0, 255, 0), sysfont.sysfont)
        tft.text((15, 95), "Target clear", tft.color(255, 192, 203), sysfont.sysfont)
        rwr_search()
    #object is between 35 and 50 cm, rwr_lock()
    elif 35 <= object <= 50:
        rgb_color(255, 120, 0) #yellowish/ dim golden
        print(f"RWR: [WARNING] Target Locked at {object}cm! Approach Stopped - Danger Threshold!!")
        tft.text((15, 75), "RWR: WARNING!", tft.color(0, 255, 0), sysfont.sysfont)
        tft.text((15, 95), "Target Locked!", tft.color(255, 192, 203), sysfont.sysfont)
        rwr_lock()
    #object is very close less that 35 cm, rwr_warning, acts as the final warning before imminent doom
    elif object <= 35:
        rgb_color(255, 0, 0) #red
        print(f"RWR: [CRITICAL] COLLISION AT {object}cm! IMPACT IMMINENT - REVERSE NOW!")
        tft.text((15, 75), "CRITICAL THREAT!", tft.color(0, 255, 0), sysfont.sysfont)
        tft.text((15,75), "REVERSE NOW!", tft.color(255, 192, 203), sysfont.sysfont)
        rwr_warning()
    else:
        #incase something is not working as it should 
        print("error")
        
    
try:
    tft.fill(tft.color(0, 0, 0))
    tft.text((19, 10), "DISTANCE SENSOR", tft.color(255, 255, 255), sysfont.sysfont)
    while True:
        distance = ultra_sonic.distance_cm()
        
        distance_text = f"Distance: {distance:.1f} cm  "
        tft.text((15, 50), distance_text, tft.color(255, 0, 0), sysfont.sysfont)
        
        detect_distance(distance)
        
        time.sleep_ms(100)
#catches KeyboardInterrupt caused by Thonny stop button during execution of code
except KeyboardInterrupt:
    print("\nProgram stopped no erorrs.")
    
finally:
    #stop the buzzer so it dosen't go for ever
    buzzer.duty_u16(0)
    rgb_color(0, 0, 0)