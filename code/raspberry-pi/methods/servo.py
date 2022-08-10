
import RPi.GPIO as GPIO
import time as time
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT) # tilt
GPIO.setup(12, GPIO.OUT) # pan
 
servo = GPIO.PWM(13,500)
servo.start(0)

try:
   while True:
     for dc in range(0,100,1): # 0 to 100 duty cycle range, third param is step
        servo.ChangeDutyCycle(dc)
        time.sleep(0.5)
     for dc in range(100,0,-1): # this makes it jump back to other position at full speed
        servo.ChangeDutyCycle(dc)
        time.sleep(0.5)
except KeyboardInterrupt:
   pass

servo.stop()
GPIO.cleanup()