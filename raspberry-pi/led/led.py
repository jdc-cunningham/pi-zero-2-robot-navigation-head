import RPi.GPIO as GPIO

class Led():
  def __init__(self):
    self.led_pin = 6

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(self.led_pin, GPIO.OUT)

  def on(self):
    GPIO.output(self.led_pin, GPIO.HIGH)

  def off(self):
    GPIO.output(self.led_pin, GPIO.LOW)
