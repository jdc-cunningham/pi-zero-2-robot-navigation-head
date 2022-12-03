# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import os
import pigpio
import time

pi = pigpio.pi()
pan_servo = 12
tilt_servo = 13 

def center_servos():
  pi.set_servo_pulsewidth(pan_servo, 1460)
  pi.set_servo_pulsewidth(tilt_servo, 1290)

def move_servo(which_servo, start_ms, end_ms):
  iter_sign = -5 if (start_ms > end_ms) else 5

  for pw in range(start_ms, end_ms, iter_sign):
    pi.set_servo_pulsewidth(which_servo, pw)
    time.sleep(0.02)

def take_photo(name):
  os.system(f"libcamera-still --rotation 180 -o panorama/{name}.jpg")

def generate_panorama():
  center_servos()
  
  # look left
  pi.set_servo_pulsewidth(pan_servo, 1760)
  
  # do vertical slice set of shots
  time.sleep(1)
  take_photo('left_top')
  pi.set_servo_pulsewidth(tilt_servo, 950)
  time.sleep(1)
  take_photo('left_middle')
  pi.set_servo_pulsewidth(tilt_servo, 650)
  time.sleep(1)
  take_photo('left_bottom')

  # look middle
  pi.set_servo_pulsewidth(pan_servo, 1460)
  time.sleep(1)
  take_photo('center_bottom')
  pi.set_servo_pulsewidth(tilt_servo, 950)
  time.sleep(1)
  take_photo('center_middle')
  time.sleep(1)
  pi.set_servo_pulsewidth(tilt_servo, 1290)
  time.sleep(1)
  take_photo('center_top')

  # look right
  pi.set_servo_pulsewidth(pan_servo, 1160)
  time.sleep(1)
  take_photo('right_top')
  pi.set_servo_pulsewidth(tilt_servo, 950)
  time.sleep(1)
  take_photo('right_middle')
  pi.set_servo_pulsewidth(tilt_servo, 650)
  time.sleep(1)
  take_photo('right_bottom')

  # recenter
  pi.set_servo_pulsewidth(tilt_servo, 1290)
  pi.set_servo_pulsewidth(pan_servo, 1460)

generate_panorama()
