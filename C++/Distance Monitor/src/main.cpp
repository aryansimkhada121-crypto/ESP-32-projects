#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <HCSR04.h>

// Initialize the ST7735 display
#define tft_cs 5
#define tft_rst 4
#define tft_ao 2

Adafruit_ST7735 tft = Adafruit_ST7735(tft_cs, tft_ao, tft_rst);

// initalize the sensor (trig, echo)
UltraSonicDistanceSensor ultra_sonic(21,19);

// initialize the buzzer
#define buzzer 12

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

//sound function to generate sound
void play_sound(int freq, int duration_ms){
 if (freq <= 0) {
    noTone(buzzer);
  } 
  else {
        tone(buzzer, freq);
    }
  delay(duration_ms);
}

/* 
RWR-search,lock, and warning/launch (RADAR WARNING RECIVER) sounds (as realstic as it can be)
*/

void rwr_search(){
  //Slow tone 
  play_sound(2600, 30);
  play_sound(0, 40);
  play_sound(2600, 30);
  play_sound(0, 900);

}

void rwr_lock(){
  //Faster tone 
  for (int i = 0; i < 6; i++) {
    play_sound(2800, 40);
    play_sound(2300, 40);
  }
  play_sound(0, 200);

}

void rwr_warning(){
  // very fast tone (object is very close imminent threat warning from RWR)
  // verrrry hyper-aggressive, chaotic tone to maximize the imminent threat incoming, trying to replicate real life threat in combats cases
  for (int burst = 0; burst < 3; burst++) {
    for (int freq = 1800; freq < 3200; freq += 200) {
      play_sound(freq, 5);
      }
    for (int i = 0; i < 4; i++) {
      play_sound(3500, 15);
      play_sound(400, 10); // Gritty low tone drop
      }
    play_sound(0, 20);

    }
}

void detect_distance(float obj){
  if (obj < 0) {
    Serial.println("error");
    return;
  }
  tft.setCursor(5, 75); 
  // object is farther that 50 cm, play rwr_search()
  if (obj >= 50){
    rgb_color(0, 150, 0);
    tft.setTextColor(ST7735_CYAN, ST7735_BLACK);
    tft.println("RWR: SCANNING         ");
    rwr_search();
    }
  else if (obj >= 35 && obj <= 50){
    rgb_color(0, 120, 255);
    tft.setTextColor(ST7735_CYAN, ST7735_BLACK);
    tft.println("RWR: WARNING      ");
    rwr_lock();
  }
  else if(obj <= 35){
    rgb_color(255, 0, 0);
    tft.setTextColor(ST7735_CYAN, ST7735_BLACK);
    tft.println("RWR: CRITICAL THREAT     ");
    rwr_warning();
  }
}

void setup() {
  Serial.begin(115200);

  tft.initR(INITR_BLACKTAB); 
  tft.setCursor(20, 10);
  tft.fillScreen(ST7735_BLACK);
  tft.setTextSize(1);
  tft.println("Distance Sensor!");

  
  pinMode(buzzer, OUTPUT);

  pinMode(red_led_pin, OUTPUT); 
  pinMode(green_led_pin, OUTPUT);
  pinMode(blue_led_pin, OUTPUT);

}

void loop() {
  float distance = ultra_sonic.measureDistanceCm();
  detect_distance(distance);

  tft.setCursor(15, 85);
  tft.setTextColor(ST7735_GREEN, ST7735_BLACK);
  tft.print("DST: ");
  tft.print(distance, 1);
  tft.println(" cm   ");

}