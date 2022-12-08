#include "Arduino.h"
#include "ultrasonic.h"

Ultrasonic::Ultrasonic(int TRIG, int ECHO){
  trigPin = TRIG;
  echoPin = ECHO;
}

void Ultrasonic::init(){
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void Ultrasonic::Tone(uint16_t frequency, uint16_t duration){
  unsigned long startTime = millis();
  unsigned long halfPeriod = 1000000L / (frequency * 2);
  pinMode(11, OUTPUT);
  while (millis() - startTime < duration)
  {
    digitalWrite(11, HIGH);
    delayMicroseconds(halfPeriod);
    digitalWrite(11, LOW);
    delayMicroseconds(halfPeriod);
  }
  pinMode(11, INPUT);
}

unsigned int Ultrasonic::getDistance(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  int distances = pulseIn(echoPin, HIGH) / 58.2;
  if(distances > 100) {
    distances = 100;
  }
  if(distances <= 10) {
    Tone(1000, 100);
  }
  return distances;
}
