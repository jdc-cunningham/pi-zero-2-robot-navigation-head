# sensor: TFmini-s UART/i2c
# this is a single-point lidar
# main measurement code sourced from this thread
# https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=261501&sid=bd5a2075068a119ae047064d2fb299d4#p1594877

import serial
import time

class LidarSensor:
  def __init__(self, param):
    # self.param = param
    self.ser = serial.Serial('/dev/serial0',115200,timeout = 1)

  def get_measurement(self):
    ser = self.ser
    #ser.write(0x42)
    ser.write(bytes(b'B'))
    #ser.write(0x57)
    ser.write(bytes(b'W'))

    #ser.write(0x02)
    ser.write(bytes(2))
    #ser.write(0x00)
    ser.write(bytes(0))
    #ser.write(0x00)
    ser.write(bytes(0))
    #ser.write(0x00)
    ser.write(bytes(0))        
    #ser.write(0x01)
    ser.write(bytes(1))         
    #ser.write(0x06)
    ser.write(bytes(6))

    if (ser.in_waiting >= 9):
      if((b'Y' == ser.read()) and ( b'Y' == ser.read())):
        Dist_L = ser.read()
        Dist_H = ser.read()
        Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
        for i in range (0,5):
          ser.read()
          return Dist_Total