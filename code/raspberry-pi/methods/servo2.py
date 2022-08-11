# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import pigpio

# 1500 is midpoint
# 2500 is max
pi = pigpio.pi()

# 12 pan
# 13 tilt

pi.set_servo_pulsewidth(12, 1500)
pi.set_servo_pulsewidth(13, 1080)

