import sys
import time
sys.path.append('/home/pi/chisel-bot-2/code/raspberry-pi')

# from methods.start_imu import *
from sensors.Sensors import *
from servo import boot_center, look_right, look_left

sensors = Sensors()

boot_center()
time.sleep(2)
look_left(16.2) # know it's 21 deg to the right

print('distance to box: ' + str(sensors.tof.get_distance()) + ', ' + str(sensors.lidar.get_distance()))
