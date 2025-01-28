from servo.servo import Servo
from narrow_angle_sensor.sensor import NarrowSensor
from wide_angle_sensor.sensor import WideSensor
from led.led import Led
from imu_sensor.imu_sensor import IMUSensor
from navigation.navigation import Navigation
from socket_server.socket_server import SocketServer
from socket_client.socket_client import SocketClient

import os

# assumes Raspberry Pi/Linux
if (os.name == "posix"):
  web_ui_socket = SocketServer()
  vehicle_socket = SocketClient()
  light = Led()
  motion = Servo()
  narrow_angle_sensor = NarrowSensor()
  wide_angle_sensor = WideSensor()
  navigation = Navigation(motion, wide_angle_sensor, narrow_angle_sensor, vehicle_socket)

  light.off()
  motion.boot_center()
  # navigation.scan_floor()
  navigation.full_floor_scan()
else:
  '''
  here you can run code/mock things without the hardware
  if your non-raspberry-pi OS is linux this may cause a problem eg. be posix
  '''
  print("windows")

