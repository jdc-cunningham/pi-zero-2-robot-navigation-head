# https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
from gpiozero import Servo
from time import sleep

servo = Servo(13)
val = -1

try:
 while True:
  servo.value = val
  sleep(1)
  val = val + 0.1
  if val > 1:
    val = -1
except KeyboardInterrupt:
  print("Program stopped")

