// 0: stop, 1: forward, 2: right, 3: left, 4: backward
const int Speed[5][2] = {{0, 0}, {150, 150}, {150, 0},
                              {0, 150}, {-150, -150}};

void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop() {
  serialRead();
}

void serialRead() {
  if(Serial.available()) {
  String str = Serial.readStringUntil('\n');
  if(str == "0"){
    motorSpeed(Speed[0][0], Speed[0][1]);
  }
  else if(str == "1"){
    motorSpeed(Speed[1][0], Speed[1][1]);
  }
  else if(str == "2"){
    motorSpeed(Speed[2][0], Speed[2][1]);
  }
  else if(str == "3"){
    motorSpeed(Speed[3][0], Speed[3][1]);
  }
  else if(str == "4"){
    motorSpeed(Speed[4][0], Speed[4][1]);
  }
 }
}

void motorSpeed(int left, int right) {
  analogWrite(3, left);
  digitalWrite(4, LOW);
  analogWrite(5, right);
  digitalWrite(6, LOW);
}
