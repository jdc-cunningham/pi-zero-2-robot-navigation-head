import json
import time

from threading import Thread
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

class IMU():
  def __init__(self):
    self.mpu = MPU9250(
      address_ak=AK8963_ADDRESS,
      address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
      address_mpu_slave=None,
      bus=1,
      gfs=GFS_1000,
      afs=AFS_8G,
      mfs=AK8963_BIT_16,
      mode=AK8963_MODE_C100HZ)
    self.sample_data = json

    self.mpu.configure() # Apply the settings to the registers.

  def continuous_imu_sample(self):
    while True:
      sample = [
        self.mpu.readAccelerometerMaster(),
        self.mpu.readGyroscopeMaster(),
        # mpu.readMagnetometerMaster() # not used indoors
      ]

      self.sample_data = json.dumps(sample)

      time.sleep(self.sample_rate)

  def start_sampling_imu(self):
    Thread(target=self.continuous_imu_sample, args=()).start() # does this thread die when parent dies?