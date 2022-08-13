# this is for the funny video, it's manually programmed
# this will command the buggy to move into frame then stop
# pan/tilt platform will look around
# buggy turns and drives away out of frame

import sys

sys.path.insert(1, '/home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/methods') # stupidly long paths

from servo import tmp_look_around

tmp_look_around()
