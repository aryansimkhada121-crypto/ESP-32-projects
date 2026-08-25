#include <Arduino.h>
#include <Wire.h>             // For I2C 
#include <Adafruit_GFX.h>     // Graphics and font 
#include <Adafruit_SSD1306.h> // Adafruit driver

//initalize oled
#define screen_height 64
#define screen_width 128

Adafruit_SSD1306 oled(screen_width, screen_height, &Wire, -1);

//initalize LDR
constexpr int adc_pin = 34;

// tested low and high limits

/*
Bright Room: Above 2500 (~2.0V)
Dim Room: Between 1200 and 2500 (~1.0V to ~2.0V)
Dark Room: Below 1200 (less than ~1.0V)
*/

const int sensorMin = 505;
const int sensorMax = 3535;

// initialize the rbg led pins
#define red_led_pin 33
#define green_led_pin 25
#define blue_led_pin 26

//#color function in (r,g,b) format 
void rgb_color(int r, int g, int b)
{
  analogWrite(red_led_pin, r);
  analogWrite(green_led_pin, g);
  analogWrite(blue_led_pin, b);
}

//#check light levels

void light_levels(int light){
  //Wipe the screen clean before drawing anything new
  oled.clearDisplay();

  //Bright Room: Above 2500 (~2.0V)
  if(light > 2500){
    oled.setCursor(0, 20);
    oled.print("Room is bright");
    oled.display();
    rgb_color(0, 255, 0);
  } 
  //Dim Room: Between 1200 and 2500 (~1.0V to ~2.0V)
  else if(light > 1200 && light <= 2500){
    oled.setCursor(0, 20);
    oled.print("Room is dim");
    oled.display();
    rgb_color(255, 255, 0);
  }
  //Dark Room: Below 1200 (less than ~1.0V)
  else if(light < 1200){
    oled.setCursor(0, 20);
    oled.print("Room is dark");
    oled.display();
    rgb_color(255, 0, 0);
  }
  else{
    Serial.println("something is wrong");
  }
}

void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22, 400000);

  delay(100);

  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)){
    Serial.println(F("SSD1306 allocation failed"));
    delay(2000);
    for(;;);
  }

  oled.clearDisplay();
  oled.display();
  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);

  analogSetPinAttenuation(adc_pin, ADC_11db);

  pinMode(red_led_pin, OUTPUT); 
  pinMode(green_led_pin, OUTPUT);
  pinMode(blue_led_pin, OUTPUT);
}

void loop() {
  int digital_value = analogRead(adc_pin);
  Serial.printf("ADC Raw Value: %d\n ", digital_value);
  float volt = 3.3 * ((float)digital_value / 4095.0);
  Serial.printf("Voltage Value: %.2fV\n ", volt);

  light_levels(digital_value);

  delay(1000);
}