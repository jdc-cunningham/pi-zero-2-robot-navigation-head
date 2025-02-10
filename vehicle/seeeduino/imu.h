#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

#define OUTPUT_READABLE_ACCELGYRO

int16_t ax, ay, az;
int16_t gx, gy, gz;
bool blinkState;

void setupIMU()
{
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin(); 
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif

  mpu.initialize();

  Serial.println("Testing MPU6050 connection...");

  if(mpu.testConnection() ==  false){
    Serial.println("MPU6050 connection failed");
    while(true);
  }
  else{
    Serial.println("MPU6050 connection successful");
  }

  // set offsets from running zero_imu.ino
  mpu.setXAccelOffset(-4); //Set your accelerometer offset for axis X
  mpu.setYAccelOffset(-8.5); //Set your accelerometer offset for axis Y
  mpu.setZAccelOffset(4.5); //Set your accelerometer offset for axis Z
  mpu.setXGyroOffset(0);  //Set your gyro offset for axis X
  mpu.setYGyroOffset(-3.5);  //Set your gyro offset for axis Y
  mpu.setZGyroOffset(0);  //Set your gyro offset for axis Z
}

String getAccelX()
{
  mpu.getAcceleration(&ax, &ay, &az);
  return String(ax);
}