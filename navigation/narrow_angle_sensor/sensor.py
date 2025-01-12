import time

class NarrowSensor():
  def __int__(self):
    self.name = "TFmini-s"
    self.serial_port = "/dev/serial0" # Raspberry Pi normal serial port
    self.serial_rate = 115200 # TFMini-Plus default baud
    self.sensor = tfmP

    self.setup()

  def setup(self):
    self.sensor.begin(self.serial_port, self.serial_rate)
    self.sensor.sendCommand( SOFT_RESET, 0)
    time.sleep(0.5)
    self.sensor.sendCommand(SET_FRAME_RATE,FRAME_20)
    time.sleep(0.5) # 1 second lag per scan

  def get_distance(self):
    self.sensor.getData()
    return self.sensor.dist * 0.39
