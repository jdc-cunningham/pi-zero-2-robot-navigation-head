sys.path.append('/home/pi/chisel-bot-2/code/raspberry-pi')

# from methods.start_imu import *
from sensors.Sensors import *
from servo import pan_control, tilt_control

sensors = Sensors()
