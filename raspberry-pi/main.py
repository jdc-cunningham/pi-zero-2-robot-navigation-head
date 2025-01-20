from servo.servo import Servo
from narrow_angle_sensor.sensor import NarrowSensor
from wide_angle_sensor.sensor import WideSensor
from led.led import Led
from imu_sensor.imu_sensor import IMUSensor
from navigation.navigation import Navigation
from websocket.websocket import Websocket

socket = Websocket()
light = Led()
motion = Servo()
# wide_angle_sensor = WideSensor()
# navigation = Navigation(motion, wide_angle_sensor)

light.off()
motion.boot_center()
# navigation.scan_floor()

