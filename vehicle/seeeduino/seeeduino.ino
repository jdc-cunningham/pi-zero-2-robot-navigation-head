#include "esp-01.h"
#include "motion.h"
#include "imu.h"

#include <vector>

void setup()
{
  Serial.begin(115200);
  setupEspSerial();
  setupIMU();
  setupServos();
}

std::vector<int> imu_x_samples;
String turnTo = "";
unsigned long elapsedTimeMs = 0;
bool stop = false;
int imuThreshold = 10;
double imu_x_avg = 0.0;
int centerImuAvg = 0;

void update_imu_samples(int sample)
{
  // if (centerImuAvg && imu_x_samples.size() == 5)
  // {
  //   imu_x_samples.erase(imu_x_samples.begin());
  // }

  imu_x_samples.push_back(sample);
}

double imu_samples_avg()
{
  double sum = 0.0;

  for (int elem : imu_x_samples) {
      sum += elem;
  }

  return sum / imu_x_samples.size();
}

void sampleImu()
{
  int imu_x_now = getRotationX();

  // Serial.println(imu_x_now);
  if (!centerImuAvg)
  {
    update_imu_samples(imu_x_now);
  }

  imu_x_avg = imu_samples_avg();

  if (imu_x_samples.size() == 100 && !centerImuAvg)
  {
    centerImuAvg = imu_x_avg;
  }

  // Serial.println(String(imu_x_avg) + " " + String(imu_x_now));
  if (!centerImuAvg) {
    return;
  }

  if (imu_x_now + centerImuAvg > 0)
  {
    turnTo = "left";
  } else
  {
    turnTo = "right";
  }

  // Serial.println(turnTo + " " + imu_x_now + " " + centerImuAvg);
}

void sampleGyro()
{
  Serial.println(getRotationX());
}

// command string samples
// mf_10 means move forward 10 inches
// the commands come from esp-01.h
void loop()
{
  if (!centerImuAvg)
  {
    sampleImu();
  }

  if (elapsedTimeMs % 20 == 0)
  {
    turnTo = "center";
  }

  // sampleGyro();

  // checkMessages();

  if (centerImuAvg && motionCommand)
  {
    sampleImu();
    parseMotionCommand(motionCommand, turnTo, stop);
  }

  elapsedTimeMs += 10;

  // Serial.println(elapsedTimeMs);

  delay(10);
}
