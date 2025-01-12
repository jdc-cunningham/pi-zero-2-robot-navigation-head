from servo.servo import Servo
import tfmplus.tfmplus as tfmP
from tfmplus.tfmplus import *
from narrow_angle_sensor.sensor import NarrowSensor
from wide_angle_sensor.sensor import WideSensor

# servo = Servo()
# servo.boot_center()

n_sensor = NarrowSensor()
w_sensor = WideSensor()

print(n_sensor.get_distance())
print(w_sensor.get_distance())


