#include "motion.h"
#include "esp-01.h"

void setup()
{
  Serial.begin(115200);
  setupEspSerial();
  setupServos();
}

void loop()
{
  // this is where no threading is a problem
  if (motionIncrementer == maxMotionVal)
  {
    activeDirection = "";
    motionIncrementer = 0;
    stopMoving();
  }

  if (activeDirection == "")
  {
    checkMessages();
  }

  if (activeDirection == "forward")
  {
    moveForward();
    delay(motionDelay);
    motionIncrementer += 1;
  }

  if (activeDirection == "left")
  {
    turnLeft();
    delay(motionDelay);
    motionIncrementer += 1;
  }

  if (activeDirection == "right")
  {
    turnRight();
    delay(motionDelay);
    motionIncrementer += 1;
  }

  if (activeDirection == "back")
  {
    moveBackward();
    delay(motionDelay);
    motionIncrementer += 1;
  }
}