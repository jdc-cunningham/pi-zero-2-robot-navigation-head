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
std::vector<int> twCenterRange = [356, 358];

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
  } else {
    if (elapsedTime % 100 == 0)
    {
      tailwheelAngleSamples.push_back(convertRawAngleToDegrees(ams5600.getRawAngle()));
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
    Serial.println(String(elapsedTime) + " " + String(motionStartTime) + " " + String(motionStopTime));

    if ((elapsedTime - motionStartTime) > motionStopTime)
    {
      stopMoving();

      Serial.println("stopped moving");
      Serial.println(String(tailwheelAngleSamples.size()));

      for (int i = 0; i < tailwheelAngleSamples.size(); i++)
      {
        Serial.println(String(tailwheelAngleSamples[i]));
      }
    }
  }
}
