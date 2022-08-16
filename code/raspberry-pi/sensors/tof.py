# https://github.com/johnbryanmoore/VL53L0X_rasp_python/blob/master/python/VL53L0X_example.py
import time
import sys

sys.path.append('/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/sensors/VL53L0X_rasp_python')

from python import VL53L0X

def get_distance():
  tof = VL53L0X.VL53L0X()
  tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
  distance = tof.get_distance()
  tof.stop_ranging()
  return (distance / 10) * 0.39 # cm to in (1 -> 0.393701)
