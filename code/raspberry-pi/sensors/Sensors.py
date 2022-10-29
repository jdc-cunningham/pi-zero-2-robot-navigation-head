import sys

from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/sensors')

from . import tof
import RPi.GPIO as GPIO
import time
import subprocess
import tfmplus as tfmP # Import the `tfmplus` module v0.1.0
from tfmplus import *    # and command and paramter defintions

from os.path import exists
from methods.imu import * 

class Sensors:
  def __init__(self):
    self.camera = self.Camera()
    self.tof = self.Tof()
    self.lidar = self.Lidar()
    self.imu = self.Imu()

  class Camera():
    def __init__(self):
      self.name = "Raspberry Pi Camera Module V2 8MP"
      self.led_pin = 6 # this is used in low light

      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(6, GPIO.OUT)

    def led_on(self):
      GPIO.output(self.led_pin, GPIO.HIGH)

    def led_off(self):
      GPIO.output(self.led_pin, GPIO.LOW)

    def take_photo(self):
      filename = str(int(time.time())) + ".jpg"
      # rotate 180deg since camera mounted upside down
      subprocess.run(["libcamera-jpeg", "--rotation", "180", "-o", filename])
      return exists(filename)

  class Tof():
    def __init__(self):
      self.name ="Pololu VL53L0X"
      # self.tof = VL53L0X.VL53L0X()
      self.tof = tof

    def get_distance(self):
      return self.tof.get_distance()

  class Lidar():
    def __init__(self):
      self.name = "TFmini-s"
      self.serial_port = "/dev/serial0" # Raspberry Pi normal serial port
      self.serial_rate = 115200 # TFMini-Plus default baud
      self.lidar = tfmP

      self.setup_lidar()

    # this is from tfmp_test.py
    def setup_lidar(self):
      self.lidar.begin(self.serial_port, self.serial_rate)
      self.lidar.sendCommand( SOFT_RESET, 0)
      time.sleep(0.5)
      self.lidar.sendCommand(SET_FRAME_RATE,FRAME_20)
      time.sleep(0.5) # 1 second lag per scan

    def get_distance(self):
      self.lidar.getData()
      return self.lidar.dist * 0.39

  # I think this will always be running as a thread
  # if not store data in memory I guess during a motion
  class Imu():
    def __init__(self):
      self.mpu_sample = None
      self.mpu = imu_setup()
      self.name = "MPU9250"
      # self.measurements = []

      # start sampling imu continuously, send to socket as well
      start_sampling_imu(self)

    def get_all(self):
      return [
        self.mpu.readAccelerometerMaster(),
        self.mpu.readGyroscopeMaster(),
        self.mpu.readMagnetometerMaster()
      ]

    def get_single(self, type = 0): # 0, 1, 2 :  accel, gyro, mag
      if (type == 0):
        return self.mpu.readAccelerometerMaster()
      elif (type == 1):
        return self.mpu.readGyroscopeMaster()
      else:
        return self.mpu.readMagnetometerMaster()

    # def start_sampling(self):
      # self.measurements.append() # have to think about this
