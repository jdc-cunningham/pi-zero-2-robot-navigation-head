#include <Servo.h>

// continuous rotation servos
struct servo {
  int pin;
  int stopPos;  // degrees
  int speedPos; // degrees
  int runTime;  // seconds
  Servo servo;  // seems silly, was looking for a self/this equivalent
};

servo leftServo = servo{0, 90, 85, 1};
servo rightServo = servo{3, 90, 97, 1};

bool motionInProgress = false;

void setupServos()
{
  leftServo.servo.attach(leftServo.pin);
  rightServo.servo.attach(rightServo.pin);
}

void stopMoving()
{
  if (motionInProgress) return;

  leftServo.servo.write(leftServo.stopPos);
  rightServo.servo.write(rightServo.stopPos);
}

void moveForward(int inches)
{
  if (motionInProgress) return;

    leftServo.servo.write(leftServo.speedPos);
    rightServo.servo.write(rightServo.speedPos);
    delay(150);
    stopMoving();
}

// ex. mf_010 for move forward 10 inches
void parseMotionCommand(String motionComand)
{
  if (motionCommand.indexOf("mf_") == 0)
  {
    int inches = motionCommand.substring(3, 6).toInt();
    moveForward(inches);
    motionCommand = "";
  }

  if (motionCommand.indexOf("mb_"))
  {
  
  }
}
