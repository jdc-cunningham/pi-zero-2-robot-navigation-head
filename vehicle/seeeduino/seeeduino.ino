#include "tail-sensor.h"
#include "esp-01.h"
#include "motion.h"

void setup()
{
  Serial.begin(115200);
  setupEspSerial();
  setupServos();
  setupTailSensor();
}

void loop()
{
  // motionCommand comes from esp-01.h
  checkMessages();
  parseMotionCommand(motionCommand, millis());
}
