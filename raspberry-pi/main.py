from servo.servo import Servo
from narrow_angle_sensor.sensor import NarrowSensor
from wide_angle_sensor.sensor import WideSensor
from led.led import Led
from imu_sensor.imu_sensor import IMUSensor
from navigation.navigation import Navigation
from socket_server.socket_server import SocketServer
from socket_client.socket_client import SocketClient

class SelfNav():
  def __init__(self):
    self.vehicle_socket = SocketClient()
    self.light = Led()
    self.motion = Servo()
    self.narrow_angle_sensor = NarrowSensor()
    self.wide_angle_sensor = WideSensor()
    self.pi_socket = SocketServer(self)
    self.navigation = Navigation(self.motion, self.wide_angle_sensor, self.narrow_angle_sensor, self.vehicle_socket, self.pi_socket)

    self.start()
  
  def start(self):
    self.light.off()
    self.motion.boot_center()
    # navigation.scan_floor()
    # navigation.full_floor_scan()

SelfNav()
