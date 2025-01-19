from servo.servo import Servo
from narrow_angle_sensor.sensor import NarrowSensor
from wide_angle_sensor.sensor import WideSensor
from led.led import Led
from imu_sensor.imu_sensor import IMUSensor

light = Led()
light.off()

motion = Servo()
motion.boot_center()

motion.pan('right', 60)
