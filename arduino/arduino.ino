#include "DHT.h"
#include <ServoTimer2.h>

// Global Variable parts
bool grabFlag = false;
bool buzzFlag = false;
const int maxDistance = 200;
const int motorPin[4] = {4, 5, 6, 7};
const int ultraPin[4] = {2, 3, 8, 9};
// 0: stop, 1: forward, 2: right, 3: left, 4: backward
const int motorSpeed[5][2] = {{0, 0}, {100, 90}, {100, 0},
                              {0, 140}, {-100, -90}};

// Object declaration parts
ServoTimer2 gripper;
DHT dht11(13, DHT11);

// Sensor Values
float temperature = 0.0;
unsigned int leftDist = 0, rightDist = 0;

void setup() {
  Serial.begin(9600);
  for(int i=0; i < 4; i++) pinMode(motorPin[i], OUTPUT);
  gripper.attach(10);
  gripper.write(angleToPulse(180));
  dht11.begin();

  pinMode(ultraPin[0], OUTPUT);
  pinMode(ultraPin[2], OUTPUT);
  pinMode(ultraPin[1], INPUT);
  pinMode(ultraPin[3], INPUT);
  // Timer initialize
  timerInit();  
}

void loop() {
  if(Serial.available()) {
    String str = Serial.readStringUntil('\n');
    if(str == "0" || str == "1" || str == "2" || str == "3") {
      digitalWrite(motorPin[0], LOW);
      digitalWrite(motorPin[3], LOW);
      analogWrite(motorPin[1], motorSpeed[str.toInt()][0]);
      analogWrite(motorPin[2], motorSpeed[str.toInt()][1]);
    }
    else if(str == "4") {
      digitalWrite(motorPin[0], HIGH);
      digitalWrite(motorPin[3], HIGH);
      analogWrite(motorPin[1], 255 + motorSpeed[str.toInt()][0]);
      analogWrite(motorPin[2], 255 +  motorSpeed[str.toInt()][1]);
    } 
    else if(str == "5") {
      grabFlag ? gripper.write(angleToPulse(180)) : gripper.write(angleToPulse(90));
      grabFlag = !grabFlag;
    }
  }
  temperature = getTemperature();
  leftDist = getDistance(ultraPin[0], ultraPin[1]);
  rightDist = getDistance(ultraPin[2], ultraPin[3]);
}

void timerInit(){
  // Timer 1 initialize
  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  // OCR1A = (CPU frequency / (Prescale * Interrupt frequency)) - 1
  OCR1A = 7812; // Sample time 0.5s
  TCCR1B |= (1 << WGM12);
  TCCR1B |= (1<<CS10) | (1<<CS12); // prescaler 1024
  TIMSK1 |= (1 << OCIE1A);
  sei();
}

ISR(TIMER1_COMPA_vect){
//  String str = "temperature, distance Left, distance right"
  String str = String(temperature) + "," + String(leftDist) + "," + String(rightDist);
  Serial.println(str);
}

int angleToPulse(int angle) {
  return map(angle, 0, 180, 750, 2250);
}

float getTemperature() {
  float temp = dht11.readTemperature();
  if(isnan(temp)) return 0.0;
  else return temp;
}

unsigned int getDistance(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  int distances = pulseIn(echo, HIGH)/58.2;
  if(distances <= 10) {
    buzzerRing();
  }
  else if(buzzFlag == true) {
    buzzerStop();
  }

  if(distances > 100){
    distances = 100;
  }
  return distances;
}

void buzzerRing(){
//  tone(11, 1000);
  myTone(11, 1000, 100);
  buzzFlag = true;
  
}

void buzzerStop() {
//  noTone(11);
  buzzFlag = false;
}

void myTone(int pin, uint16_t frequency, uint16_t duration) {
  unsigned long startTime = millis();
  unsigned long halfPeriod= 1000000L/ (frequency * 2);
  pinMode(pin,OUTPUT);
  while (millis() - startTime < duration)
  {
    digitalWrite(pin,HIGH);
    delayMicroseconds(halfPeriod);
    digitalWrite(pin,LOW);
    delayMicroseconds(halfPeriod);
  }
  pinMode(pin,INPUT);
}
