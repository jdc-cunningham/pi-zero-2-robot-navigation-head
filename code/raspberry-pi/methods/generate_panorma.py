# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import os
import pigpio
import time

pi = pigpio.pi()
pan_servo = 12
tilt_servo = 13 

def move_servo(which_servo, start_ms, end_ms):
  iter_sign = (start_ms > end_ms) ? -5 : 5

  for pw in range(start_ms, end_ms, iter_sign):
    pi.set_servo_pulsewidth(which_servo, pw)
    time.sleep(0.02)

def take_photo(name):
  os.system(f"libcamera-still -o {name}.jpg")

def generate_panorama():
  
