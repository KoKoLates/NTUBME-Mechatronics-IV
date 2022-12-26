# Arduino
`ultrasonic` 、 `interrupt`

## Interrupt
In this project, we design a `timer1` interrupt to ensure that the data of `DHT11` and `HC-SR04` could continuously send back to the server side.
```cpp
void timerInit(){   
    cli();
    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1 = 0;OCR1A = 7812; // Sample time 0.5s
    TCCR1B |= (1 << WGM12);
    TCCR1B |= (1<<CS10) | (1<<CS12); // prescaler 1024
    TIMSK1 |= (1 << OCIE1A);
    sei();
}

ISR(TIMER1_COMPA_vect){
    ...
}

```

## Ultrasonic
The self-define class for `HC-SR04` ulrtasonic sensors that more convenient for other interface to obtain distances data from ultrasonic sensor. User only have to initialize with constructor giving `trigger` and `echo` pin. The using the corresponding function `getDistance()` could obtain the distance from obstacle in center meter. 
```cpp
Ultrasonic ultra(10, 11);
int distance = ultra.getDistance();
```

## Timer Configuration
Due to the `Timer1` is setup for the PWM command for DC motor set and Interrupt serial writing. We using another libraray that using `timer2` for servo motor. Besides, the default timer for `Tone()` function is timer2. So we create a self-define `Tone()` that could use `Timer0`.

|Timer  | function |
|-------|----------|
|Timer 0| `millis()`, `delay()`, `tone()`, etc
|Timer 1| `PWM`, `Interrupt`
|Timer 2| `servoTimer2`

**Tone**
```cpp
// Self-defined tone for buzzer
void Ultrasonic::Tone(int pin, uint16_t frequency, uint16_t duration){
  unsigned long startTime = millis();
  unsigned long halfPeriod = 1000000L / (frequency * 2);
  pinMode(pin, OUTPUT);
  while (millis() - startTime < duration)
  {
    digitalWrite(pin, HIGH);
    delayMicroseconds(halfPeriod);
    digitalWrite(pin, LOW);
    delayMicroseconds(halfPeriod);
  }
  pinMode(pin, INPUT);
}
```

## Library
[**ServoTimer2**](https://github.com/nabontra/ServoTimer2) 、
[**DHT11**](https://github.com/adafruit/DHT-sensor-library) 