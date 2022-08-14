# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys
import time
import subprocess

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/methods/') # stupidly long paths

from os.path import exists
from led import led_off
from servo import boot_center
from start_imu import wake_imu

class NavUnit:
  def __init__(self):
    self.name = "UwU Navu"
    self.units = "Inches and Degrees"
    self.coordinate_system = "x,y,z where z is vertical"
    self.imu_awake = False
    self.positions = [] # {coord, time, etc...}

    # pull down camera LED, center pan-tilt servos, start IMU
    self.boot()

  def boot(self):
    led_off()
    boot_center()
    self.imu_awake = wake_imu()
    # self.take_photo()
    self.motion = self.Motion()
    self.sensors = self.Sensors()

  class Motion:
    def __init__(self):
      self.name = "UwU Navu"

    class PanTilt():
      def __init__(self):
        self.pan_servo
        self.tilt_servo
    class Wheels():
      def __init__(self):
        self.left
        self.right
        self.move_forward
        self.move_left
        self.move_right
        self.move_backward

  class Sensors:
    def __init__(self):
      self.camera = self.Camera()
      self.tof = self.Tof()
      self.lidar = self.Lidar()
      self.imu = self.Imu()

    class Camera():
      def __init__(self):
        self.name = "Raspberry Pi Camera Module V2 8MP"

      def take_photo(self):
        filename = str(int(time.time())) + ".jpg"
        # rotate 180deg since camera mounted upside down
        subprocess.run(["libcamera-jpeg", "--rotation", "180", "-o", filename])
        return exists(filename)

    class Tof():
      def __init__(self):
        self.name ="Pololu VL53L0X"

    class Lidar():
      def __init__(self):
        self.name = "TFmini-s"

    class Imu():
      def __init__(self):
        self.name = "MPU9250"

NavUnit()
