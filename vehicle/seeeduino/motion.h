#include <Servo.h>

// continuous rotation servos
struct servo {
  int pin;
  int stopPos;     // degrees
  Servo servo;     // seems silly, was looking for a self/this equivalent
};

servo leftServo = servo{0, 90};
servo rightServo = servo{3, 90};

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

// rc_084_098_1400 (move 10" forward)
// translates to: raw command, left servo to 84 deg, right servo to 98 deg both for 1400ms long
void rawCommand(String command, String turnTo, bool stop)
{
  // not how this will work just putting this in here for video demo
  if (motionInProgress) return;

  int ls_deg = command.substring(3, 6).toInt();
  int rs_deg = command.substring(7, 10).toInt();
  int stop_delay = command.substring(11, 15).toInt();

  String amount = String(ls_deg) + "," + String(rs_deg);
  // Serial.println(turnTo + " ");

  if (turnTo == "left")
  {
    ls_deg = 86;
  }

  if (turnTo == "right")
  {
    rs_deg = 96;
  }

  leftServo.servo.write(ls_deg);
  rightServo.servo.write(rs_deg);

  if (stop)
  {
    stopMoving();
  }
}

// ex. mf_010 for move forward 10 inches
void parseMotionCommand(String motionCommand, String turnTo, bool stop)
{
  if (motionCommand.indexOf("rc_") == 0)
  {
    rawCommand(motionCommand, turnTo, stop);
  }
}
