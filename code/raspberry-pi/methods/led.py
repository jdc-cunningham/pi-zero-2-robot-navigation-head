# this is a white LED that helps take pictures indoors

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6, GPIO.OUT)

def led_on():
  GPIO.output(6, GPIO.HIGH)

def led_off():
  GPIO.output(6, GPIO.LOW)
