# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import pigpio

pi = pigpio.pi()

pan_servo = 12
tilt_servo = 13

# 1500 is midpoint
# 2500 is max

def boot_center():
  pi.set_servo_pulsewidth(pan_servo, 1440) # > 1500, left
  pi.set_servo_pulsewidth(tilt_servo, 1090) # < 1500 up
