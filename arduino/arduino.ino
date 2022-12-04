
String str = "";
// 0: stop, 1: forward, 2: right, 3: left, 4: backward
const int motorSpeed[5][2] = {{0, 0}, {150, 150}, {150, 0},
                              {0, 150}, {-150, -150}};

void setup() {
    Serial.begin(9600);
}

void loop() {
    serialRead();
    serialWrite();
}

void serialRead() {
    if(Serial.available()) {
        str = Serial.readStringUntil('\n');
    }else {
        str = "";
    }
}

void serialWrite() {
    if(str != ""){
        Serial.println(str);
    }
}
