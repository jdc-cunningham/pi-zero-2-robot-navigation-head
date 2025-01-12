import sys

sys.path.insert(1, '/home/pi/pi-zero-2-robot-navigation-head/navigation')

from VL53L0X.python import VL53L0X

class WideSensor():
  def __init__(self):
    self.sensor = VL53L0X.VL53L0X()

  def get_distance(self):
    self.sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    self.sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    distance = self.sensor.get_distance()
    self.sensor.stop_ranging()
    return (distance / 10) * 0.39 # cm to in (1 -> 0.393701)
