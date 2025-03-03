#include <Servo.h>
#include <vector>

// continuous rotation servos
struct servo {
  int pin;
  int stopPos;     // degrees
  Servo servo;     // seems silly, was looking for a self/this equivalent
};

servo leftServo = servo{0, 90};
servo rightServo = servo{3, 90};
bool motionInProgress = false;
unsigned long motionStartTime = 0;
int motionStopTime = 0;
int ls_deg = 0;
int rs_deg = 0;
int stop_delay = 0;
int tailwheelCenterAngle = 214; // left decreases, right increases
int steeringCorrectionDelay = 100; // ms

std::vector<int> tailwheelAngleSamples;

void setupServos()
{
  leftServo.servo.attach(leftServo.pin);
  rightServo.servo.attach(rightServo.pin);
}

void stopMoving()
{
  leftServo.servo.write(leftServo.stopPos);
  rightServo.servo.write(rightServo.stopPos);

  motionInProgress = false;
  motionCommand = "";
}

// based on straight command servo angles
void slightRight()
{
  ls_deg = 83;
}

void slightLeft()
{
  rs_deg = 99;
}

void goStraight()
{
  ls_deg = 84;
  rs_deg = 98;
}

// rc_084_098_1400 (move 10" forward)
// translates to: raw command, left servo to 84 deg, right servo to 98 deg both for 1400ms long
void rawCommand(String command, unsigned long elapsedTime)
{
  if (!motionInProgress)
  {
    ls_deg = command.substring(3, 6).toInt();
    rs_deg = command.substring(7, 10).toInt();
    stop_delay = command.substring(11, 15).toInt();
    motionStartTime = elapsedTime;
    motionStopTime = stop_delay;
    motionInProgress = true;
  }

  // use tailwheel feedback to go straight
  if (command.indexOf("rc_084_098_") == 0)
  {
    // the delay is for the tailwheel to straighten itself out
    if (elapsedTime - motionStartTime >= steeringCorrectionDelay)
    {
      int tailwheelAngle = int(convertRawAngleToDegrees(ams5600.getRawAngle()));

      if (tailwheelAngle < tailwheelCenterAngle) {
        slightRight();
      } else if (tailwheelAngle > tailwheelCenterAngle) {
        slightLeft();
      } else {
        goStraight();
      }
    }
  }

  if (motionInProgress)
  {
    leftServo.servo.write(ls_deg);
    rightServo.servo.write(rs_deg);
  }
}

// ex. mf_010 for move forward 10 inches
void parseMotionCommand(String motionCommand, unsigned long elapsedTime)
{
  if (motionCommand.indexOf("rc_") == 0)
  {
    rawCommand(motionCommand, elapsedTime);
  }

  if (motionInProgress)
  {
    if ((elapsedTime - motionStartTime) > motionStopTime)
    {
      stopMoving();
    }
  }
}
