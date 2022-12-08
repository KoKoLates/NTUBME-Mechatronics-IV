#include "DHT.h"
#include <NewPing.h>
#include <ServoTimer2.h>

// Global Variable parts
bool grabFlag = false;
const int maxDistance = 200;
const int motorPin[4] = {4, 5, 6, 7};
const int ultroPin[4] = {2, 3, 8, 9};
// 0: stop, 1: forward, 2: right, 3: left, 4: backward
const int motorSpeed[5][2] = {{0, 0}, {100, 100}, {100, 0},
                              {0, 100}, {-100, -100}};

// Object declaration parts
ServoTimer2 gripper;
DHT dht11(13, DHT11);
NewPing ultroLeft(ultroPin[0], ultroPin[1], maxDistance);
NewPing ultroRight(ultroPin[2], ultroPin[3], maxDistance);

// Sensor Values
float temperature = 0.0;
unsigned int leftDist = 0, rightDist = 0;

void setup() {
  Serial.begin(9600);
  for(int i=0; i < 4; i++) pinMode(motorPin[i], OUTPUT);
  gripper.attach(10);
  gripper.write(angleToPulse(180));
  dht11.begin();

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
    } else if(str == "4") {
      digitalWrite(motorPin[0], HIGH);
      digitalWrite(motorPin[3], HIGH);
      analogWrite(motorPin[1], 255 + motorSpeed[str.toInt()][0]);
      analogWrite(motorPin[2], 255 +  motorSpeed[str.toInt()][1]);
    } else if(str == "5") {
      grabFlag ? gripper.write(angleToPulse(180)) : gripper.write(angleToPulse(90));
      grabFlag = !grabFlag;
    }
  }
  temperature = getTemperature();
  leftDist = getDistance(ultroLeft);
  rightDist = getDistance(ultroRight);
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

unsigned int getDistance(NewPing p) {
  delay(50);
  unsigned int dis = p.ping();
  return p.convert_cm(dis);
}
