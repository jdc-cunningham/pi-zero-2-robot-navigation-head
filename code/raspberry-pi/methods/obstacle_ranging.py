import sys
import time
sys.path.append('/home/pi/chisel-bot-2/code/raspberry-pi')

# from methods.start_imu import *
from sensors.Sensors import *
from servo import boot_center, look_right

sensors = Sensors()

time.sleep(2)
boot_center()
look_right(21) # know it's 21 deg to the right

print('distance to box: ' + int(sensors.tof.get_distance()) + ', ' + int(sensors.lidar.get_distance()))