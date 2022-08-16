# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/methods') # stupidly long paths

from led import led_off
from servo import boot_center
from start_imu import wake_imu

led_off()
boot_center()
# wake_imu() # this has to go somewhere
