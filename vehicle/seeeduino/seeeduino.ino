#include "esp-01.h"
#include "motion.h"
#include "tail-sensor.h"
#include <vector>

void setup()
{
  Serial.begin(115200);
  setupEspSerial();
  setupServos();
  setupTailSensor();
}

String turnTo = "";
unsigned long elapsedTimeMs = 0;
bool stop = false;

void loop()
{
  // elapsedTimeMs += 10;

  // delay(10);

  Serial.println(String(convertRawAngleToDegrees(ams5600.getRawAngle()),DEC));
}
