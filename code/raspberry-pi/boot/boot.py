# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys

sys.path.insert(1, '/home/pi/chisel-bot-2/code/raspberry-pi/methods') # stupidly long paths

from led import led_off
from servo import boot_center

led_off()
boot_center()
