# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/methods') # stupidly long paths

from led import led_off

led_off()
