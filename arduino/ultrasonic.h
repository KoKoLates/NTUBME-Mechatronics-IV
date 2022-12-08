#ifndef _ULTRASONIC_H_
#define _ULTRASONIC_H_

#include "Arduino.h"

class Ultrasonic {
  private:
   int trigPin;
   int echoPin;

  public:
   Ultrasonic(int, int);
   void init();
   void Tone(uint16_t, uint16_t);
   unsigned int getDistance();
};

#endif //_ULTRASONIC_H_
