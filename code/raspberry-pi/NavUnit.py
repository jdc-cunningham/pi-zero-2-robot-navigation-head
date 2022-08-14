# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/methods') # stupidly long paths

import subprocess

from os.path import exists
from led import led_off
from servo import boot_center
from start_imu import wake_imu
import time

class NavUnit:
  def __init__(self):
    self.name = "UwU Navu"
    self.imu_awake = False
    self.positions = [] # [x,y]

    self.boot()

  def boot(self):
    led_off()
    boot_center()
    self.imu_awake = wake_imu()
    self.take_photo()

  def take_photo(self):
    filename = str(int(time.time())) + ".jpg"
    subprocess.run(["libcamera-still", "-o", filename])
    return exists(filename)

NavUnit()
