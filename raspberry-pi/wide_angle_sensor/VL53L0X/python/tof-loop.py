# https://github.com/johnbryanmoore/VL53L0X_rasp_python/blob/master/python/VL53L0X_example.py
import time
import sys
sys.path.insert(1, '/home/pi/test/VL53L0X_rasp_python/python/')

import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

for count in range(1,101):
    distance = tof.get_distance()
    if (distance > 0):
        print ("%d mm, %d cm, %d" % (distance, (distance/10), count))

    time.sleep(timing/1000000.00)

tof.stop_ranging()

