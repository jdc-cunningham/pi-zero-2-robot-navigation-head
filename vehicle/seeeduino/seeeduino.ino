#include "esp-01.h"
#include "tail-sensor.h"
#include "motion.h"

void setup()
{
  Serial.begin(115200);
  setupEspSerial();
  setupServos();
  setupTailSensor();
  Serial.println("run");
}

unsigned long elapsedTimeMs = 0;

void loop()
{
  // motionCommand comes from esp-01.h
  parseMotionCommand(motionCommand, elapsedTimeMs);
  delay(10);

  elapsedTimeMs += 10;
}
