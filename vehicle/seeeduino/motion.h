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

// advanced preformed string
// rc_ls_90_10_rs_90_10
// translates to: raw command, left servo 90 deg 10 ms, rs 90 deg 10 ms
// rc_090_090_0100
// translates to: raw command, left servo to 90 deg, right servo to 90 deg both for 100ms long
void rawCommand(String command)
{
  // not how this will work just putting this in here for video demo
  if (motionInProgress) return;

  int ls_deg = command.substring(3, 6).toInt();
  int rs_deg = command.substring(7, 10).toInt();
  int stop_delay = command.substring(11, 15).toInt();

  leftServo.servo.write(ls_deg);
  rightServo.servo.write(rs_deg);
  delay(stop_delay);
  stopMoving();
}

// ex. mf_010 for move forward 10 inches
void parseMotionCommand(String motionCommand)
{
  if (motionCommand.indexOf("rc_") == 0)
  {
    rawCommand(motionCommand);
  }
}
