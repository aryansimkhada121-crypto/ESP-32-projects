"""
this file was created to debug the esp32 brownout issue, when using wifi,
remove all components except esp32 and display to test and to fix the issue
"""

from machine import Pin, SPI
import time
import st7735
import sysfont
import network

led = Pin(2, Pin.OUT)

# 1. Initialize Display at 10 MHz (Prevents breadboard SPI noise)
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
tft = st7735.TFT(spi, Pin(14), Pin(27), Pin(26))
tft.initr()
tft.rgb(True)
tft.fill(tft.color(0, 0, 0))

tft.text((5, 10), "SYS: ONLINE", tft.color(0, 255, 0), sysfont.sysfont)

def connect_wifi():
    tft.text((5, 30), "Connecting WiFi...", tft.color(255, 255, 0), sysfont.sysfont)
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    try:
        wlan.config(txpower=8.5)
    except:
        pass
        
    time.sleep(1)
    wlan.connect('', '')
    
    timeout = 0
    while not wlan.isconnected() and timeout < 10:
        led.value(not led.value())
        time.sleep(1)
        timeout += 1
        
    tft.fillrect((5, 30), (120, 15), tft.color(0, 0, 0))
    if wlan.isconnected():
        tft.text((5, 30), "WiFi: OK!", tft.color(0, 255, 0), sysfont.sysfont)
    else:
        tft.text((5, 30), "WiFi: Failed", tft.color(255, 0, 0), sysfont.sysfont)

connect_wifi()

counter = 0
while True:
    # Small fillrect only around the number to prevent whole-screen flickering
    tft.fillrect((5, 60), (120, 15), tft.color(0, 0, 0))
    tft.text((5, 60), f"Loop: {counter}", tft.color(255, 255, 255), sysfont.sysfont)
    
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
    counter += 1