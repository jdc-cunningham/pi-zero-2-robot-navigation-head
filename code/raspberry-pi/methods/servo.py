# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import pigpio
import time

pi = pigpio.pi()

pan_servo = 12
tilt_servo = 13

# 1500 is midpoint
# 2500 is max

def boot_center():
  pi.set_servo_pulsewidth(pan_servo, 1440) # > 1500, left
  pi.set_servo_pulsewidth(tilt_servo, 1090) # < 1500 up

def tmp_turn_left_right():
  for pw in range(1440,1540,1): # 0 to 100 duty cycle range, third param is step
    servo.ChangeDutyCycle(pw)
    time.sleep(0.1)

tmp_turn_left_right()

# def tmp_look_around():

