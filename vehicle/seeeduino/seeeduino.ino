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
std::vector<int> tailwheelAngleSamples;

// motionCommand = "rc_084_098_1400"

void loop()
{
  // tailwheelAngle = convertRawAngleToDegrees(ams5600.getRawAngle());

  // if (motionCommand && elapsedTImeMs % 100 == 0)
  // {
  //   tailwheelAngleSamples.push_back(taillwheelAngle);
  // }

  // delay(10);

  // elapsedTimeMs += 10;
}
