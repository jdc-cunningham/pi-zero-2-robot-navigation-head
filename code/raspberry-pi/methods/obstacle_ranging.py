import time
sys.path.append('/home/pi/chisel-bot-2/code/raspberry-pi')

# from methods.start_imu import *
from sensors.Sensors import *
from servo import boot_center, look_right

sensors = Sensors()

time.sleep(2)
boot_center()
look_right(21)

print('distance to box: ' + sensors.tof.get_distance() + ', ' + sensors.lidar.get_distance())