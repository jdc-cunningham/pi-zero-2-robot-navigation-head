#include <Servo.h>

// continuous rotation servos
struct servo {
  int pin;
  int stopPos;     // degrees
  int forwardPos;  // degrees
  int backwardPos; // degrees
  Servo servo;     // seems silly, was looking for a self/this equivalent
};

servo leftServo = servo{0, 90, 85, 95};
servo rightServo = servo{3, 90, 97, 83};

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

  leftServo.servo.write(leftServo.forwardPos);
  rightServo.servo.write(rightServo.forwardPos);
  delay(800); // 1700 10 inch
  stopMoving();
}

void moveBackward(int inches)
{
  if (motionInProgress) return;

  leftServo.servo.write(leftServo.forwardPos);
  rightServo.servo.write(rightServo.forwardPos);
  delay(800); // 1700 10 inch
  stopMoving();
}

void turnLeft(int degrees)
{
  if (motionInProgress) return;

  leftServo.servo.write(leftServo.backwardPos);
  rightServo.servo.write(rightServo.forwardPos);
  delay(800);
  stopMoving();
}

void turnRight(int degrees)
{
  if (motionInProgress) return;

  leftServo.servo.write(leftServo.forwardPos);
  rightServo.servo.write(rightServo.backwardPos);
  delay(800);
  stopMoving();
}

// advanced preformed string
// rc_ls_90_10_rs_90_10
// translates to: raw command, left servo 90 deg 10 ms, rs 90 deg 10 ms
void rawCommand(String command)
{
  // not how this will work just putting this in here for video demo
  moveForward(1);
  moveForward(1);
  turnRight(1);
  moveForward(1);
  moveForward(1);
  turnRight(1);
  moveForward(1);
  moveForward(1);
  turnRight(1);
  moveForward(1);
  moveForward(1);
  turnRight(1);
}

// ex. mf_010 for move forward 10 inches
void parseMotionCommand(String motionCommand)
{
  if (motionCommand.indexOf("rc_") == 0)
  {
    rawCommand(motionCommand);
  }

  if (motionCommand.indexOf("mf_") == 0)
  {
    int inches = motionCommand.substring(3, 6).toInt();
    moveForward(inches);
    motionCommand = "";
  }

  if (motionCommand.indexOf("mb_") == 0)
  {
    int inches = motionCommand.substring(3, 6).toInt();
    moveBackward(inches);
    motionCommand = "";
  }

  if (motionCommand.indexOf("tr_") == 0)
  {
    int inches = motionCommand.substring(3, 6).toInt();
    turnRight(inches);
    motionCommand = "";
  }

  if (motionCommand.indexOf("tl_") == 0)
  {
    int inches = motionCommand.substring(3, 6).toInt();
    turnLeft(inches);
    motionCommand = "";
  }
}
