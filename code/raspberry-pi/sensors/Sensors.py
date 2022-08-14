class Sensors:
  def __init__(self):
    self.camera = self.Camera()
    self.tof = self.Tof()
    self.lidar = self.Lidar()
    self.imu = self.Imu()

  class Camera():
    def __init__(self):
      self.name = "Raspberry Pi Camera Module V2 8MP"

    def take_photo(self):
      filename = str(int(time.time())) + ".jpg"
      # rotate 180deg since camera mounted upside down
      subprocess.run(["libcamera-jpeg", "--rotation", "180", "-o", filename])
      return exists(filename)

  class Tof():
    def __init__(self):
      self.name ="Pololu VL53L0X"

  class Lidar():
    def __init__(self):
      self.name = "TFmini-s"

  class Imu():
    def __init__(self):
      self.name = "MPU9250"