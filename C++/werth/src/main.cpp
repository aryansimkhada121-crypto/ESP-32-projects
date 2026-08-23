#include <Arduino.h>
#include <DHT.h>               // dht sensor 
#include <Wire.h>             // For I2C 
#include <Adafruit_GFX.h>     // Graphics and font 
#include <Adafruit_SSD1306.h> // Adafruit driver

//initalize oled
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// initalize the pin for the dht11
const int dht_pin = 4;
#define DHTTYPE DHT11

/* DHT ---> class provided DHT library, dht --> Object name, 
(dht_pin, DHTTYPE) --> "Create a sensor object, hook it up to digital pin 2, and treat it like a DHT11 model.
*/

DHT dht(dht_pin, DHTTYPE);

// initialize the rbg led pins
const int red_led_pin = 33;
const int green_led_pin = 25;
const int blue_led_pin = 26;

//#color function in (r,g,b) format 
void rgb_color(int r, int g, int b)
{
  analogWrite(red_led_pin, r);
  analogWrite(green_led_pin, g);
  analogWrite(blue_led_pin, b);
}

// main control function that checks status 
void check_status(float tempx){
  if (tempx > 25){
    rgb_color(255, 0, 0);
    printf("It's hot!\n");
  } else if (tempx < 22 ){
    rgb_color(135, 206, 235);
    printf("It's warm!\n");
  } else{
    rgb_color(0, 0, 235);
  }
}

void setup() 
{
  Serial.begin(115200);

  Wire.begin(21, 22, 400000);

  delay(500);

  if(!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); 
  }

  oled.clearDisplay();
  oled.display();

  dht.begin();

  pinMode(red_led_pin, OUTPUT);
  pinMode(green_led_pin, OUTPUT);
  pinMode(blue_led_pin, OUTPUT);
}

void loop() {
  float temp = dht.readTemperature();
  float humi = dht.readHumidity();

  check_status(temp);

  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);

oled.setCursor(0, 0);
oled.print("Temp: ");
oled.print(temp);
oled.print(" C");

// Row 2: Humidity
oled.setCursor(0, 16); 
oled.print("Humi: ");
oled.print(humi);
oled.print(" %");

oled.display();
}