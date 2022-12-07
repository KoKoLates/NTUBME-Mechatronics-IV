bool grabFlag = false;
const int motorPin[4] = {4, 5, 6, 7};
// 0: stop, 1: forward, 2: right, 3: left, 4: backward
const int motorSpeed[5][2] = {{0, 0}, {100, 100}, {100, 0},
                              {0, 100}, {-100, -100}};

void setup() {
  Serial.begin(9600);
  for(int i=0; i < 4; i++) pinMode(motorPin[i], OUTPUT);
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
      grabServo();
    }
  } 
}

void grabServo(){
  grabFlag = !grabFlag;
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
  String str = "25, 20, 15";
//  String str = "temperature, distance Left, distance right"
//  String str = String(count) + "," + String(count + 1) + "," + String(count - 1);
  Serial.println(str);
}
