# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys
import time
import subprocess

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/methods/') # stupidly long paths

from os.path import exists
from led import led_off
from servo import boot_center
from start_imu import wake_imu
from motion import Motion
from sensors import Sensors

class NavUnit:
  def __init__(self):
    self.name = "UwU Navu"
    self.units = "inches and degrees"
    self.coordinate_system = "x,y,z where z is vertical"
    self.imu_awake = False
    self.positions = [] # {coord, time, etc...}

    self.dimensions = {
      "height": 9,
      "width": 7.75,
      "length": 11.5 # tailwheel extended out
    }

    # pull down camera LED, center pan-tilt servos, start IMU
    self.boot()

  def boot(self):
    led_off()
    boot_center()
    self.imu_awake = wake_imu()
    # self.take_photo()
    self.motion = self.Motion()
    self.sensors = self.Sensors()

NavUnit()
