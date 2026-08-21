from machine import Pin, SPI, PWM 
import time
from hcsr04 import HCSR04
import st7735
import sysfont

#initalize the ultrasonic sensor
ultra_sonic = HCSR04(trigger_pin = 26, echo_pin = 25)

#Initialize the buzzer pin (GPIO-33)
buzzer = PWM(Pin(33))

# force silent immediately on startup
buzzer.duty_u16(0)


# Initialize hardware SPI
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))

# Initialize the ST7735 display using positional arguments: (spi, DC, Reset, CS)
tft = st7735.TFT(spi, Pin(2), Pin(4), Pin(5))
tft.initr()
tft.rgb(True)

# Clear screen to black
tft.fill(tft.color(0, 0, 0))

# initialize the rbg led pins
blue_pin = PWM(Pin(19), freq=1000)
green_pin = PWM(Pin(21), freq=1000)
red_pin = PWM(Pin(22), freq=1000)

# initalize the pins for ULN driver 
pins = [ 
    Pin(13, Pin.OUT), # In-1
    Pin(12, Pin.OUT), # In-2
    Pin(14, Pin.OUT), # In-3
    Pin(27, Pin.OUT), # In-4
    ]

#Designing the Sequence Matrix
full_step_sequence = [
    [0,0,0,1],   #step 1 / row 1
    [0,0,1,0],   #step 2 / row 2
    [0,1,0,0],   #step 3 / row 3
    [1,0,0,0]    #step 4 / row 4
    ]


# rotate the stepper to 90 degree 
# 2048 steps for 360 degree, 360/4 = 512 steps, as close as possible as the stepper rotates 0.18 degree per step
def turn_90_degree():
    pattern_row = 0
    for i in range(512):
     #current 4-pin signal from the matrix for each row
        current_step = full_step_sequence[pattern_row]


    #                   pins = [ Pin13,  Pin12,  Pin14,  Pin27 ]
    #  current_signals = [   0  ,    0  ,    0  ,    1   ]
    #                        ↓          ↓        ↓               ↓
#zipped_pairs_in_memory = [ (Pin13, 0), (Pin12, 0), (Pin14, 0), (Pin27, 1) ]


    #apply the signals form each row of the matrix to physcial pins
        for pin, state in zip(pins, current_step):
            pin.value(state)

    #small delay important in giving the stepper time to move its internal gears
        time.sleep_ms(3) #3 milliseconds

    #move on to the next row
        pattern_row += 1

    #since 4 rows index = 0-3
        if pattern_row == 4:
            pattern_row = 0

# turn off all the pins to stop the coils from staying energized and overheating while standing still
    for pin in pins:
        pin.value(0)

# cm, measured with nothing in the tray
EMPTY_BASELINE = 2.0

#cm, acts as a stabilizer reducing jitter, while also acting as error margin for objects 
THRESHOLD = 1.0

# this function contorls the stepper motor, which rotates the platform, while the Hcsr-04 ultrasonic sensor detects object and plays buzzer
def active_sweep(distance_vert):
    tft.fillrect((15, 75), (150, 16), tft.color(0, 0, 0))
    #when object is detected
    if distance_vert < (EMPTY_BASELINE - THRESHOLD):
        rgb_color(255,0,0)
        print(f"Object Detected... at Distance:{distance_vert}")
        tft.text((15, 75), "Object Detected", tft.color(0, 255, 0), sysfont.sysfont)
        obj_detect()
    else:
        rgb_color(0,155,0)
        tft.text((15, 75), "SCANNING", tft.color(0, 155, 0), sysfont.sysfont)
        print("platform is clear")
        obj_search()
        


#color function in (r,g,b) format 
def rgb_color(r, g, b):
    red_pin.duty_u16(int(r * 65535 / 255))
    green_pin.duty_u16(int(g * 65535 / 255))
    blue_pin.duty_u16(int(b * 65535 / 255))

#sound function to generate sound
def play_sound(freq, duration_ms):
    if freq <= 0:
        buzzer.duty_u16(0)
    else:
        buzzer.freq(int(freq))
        buzzer.duty_u16(32768)
    time.sleep_ms(duration_ms)

def obj_detect():
    #plays sound when object is detected on the platform

    for i in range(10):
        play_sound(2200, 100)
        play_sound(0, 100)

def obj_search():
    #Slow tone (object is out of designated range)
    
    #print("RWR: Object Scanning...")
    for i in range(3):
        play_sound(1800, 50)
        play_sound(0, 450)

try:
    tft.fill(tft.color(0, 0, 0))
    tft.text((19, 10), "Stepper Motor", tft.color(255, 0, 0), sysfont.sysfont)
    while True:
        #print("stepper turning 90 degrees")
        turn_90_degree()

        distance = ultra_sonic.distance_cm()

        # hcsr04 is know for some errors, this lets the code run even if a distance value is given as None
        if distance is None:
            continue

        distance_text = f"Distance: {distance:.1f} cm  "
        tft.text((15, 50), distance_text, tft.color(0, 0, 255), sysfont.sysfont)

        print(f"distance: {distance}")
        active_sweep(distance)
        time.sleep_ms(60)

#catches KeyboardInterrupt caused by Thonny stop button during execution of code
except KeyboardInterrupt:
    print("\nProgram stopped no erorrs.")

finally:
    #stop the buzzer so it dosen't go for ever
    buzzer.duty_u16(0)
    rgb_color(0, 0, 0)