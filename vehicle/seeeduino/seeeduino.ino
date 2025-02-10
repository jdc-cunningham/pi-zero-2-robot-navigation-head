#include "esp-01.h"
#include "motion.h"
#include "imu.h"

void setup()
{
  Serial.begin(115200);
  setupEspSerial();
  setupIMU();
  setupServos();
}

// command string samples
// mf_10 means move forward 10 inches
// the commands come from esp-01.h
void loop()
{
  // Serial.println("loop");
  Serial.println(getAccelX());
  // checkMessages();

  // if (motionCommand)
  // {
  //   parseMotionCommand(motionCommand);
  // }

  delay(50);
}
