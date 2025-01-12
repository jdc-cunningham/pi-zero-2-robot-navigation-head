from servo.servo import Servo
from narrow_angle_sensor.sensor import NarrowSensor
from wide_angle_sensor.sensor import WideSensor
from led.led import Led

# servo = Servo()
# servo.boot_center()

n_sensor = NarrowSensor()
w_sensor = WideSensor()
led = Led()

led.on()

print(n_sensor.get_distance())
print(w_sensor.get_distance())

led.off()
