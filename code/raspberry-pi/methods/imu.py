import threading
import json
import time

from threading import Thread
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

mpu = None

def imu_setup():
  global mpu

  mpu = MPU9250(
      address_ak=AK8963_ADDRESS,
      address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
      address_mpu_slave=None,
      bus=1,
      gfs=GFS_1000,
      afs=AFS_8G,
      mfs=AK8963_BIT_16,
      mode=AK8963_MODE_C100HZ)

  mpu.configure() # Apply the settings to the registers.

  return mpu

def continuous_imu_sample(mpu_sample):
  while True:
    sample = [
      mpu.readAccelerometerMaster(),
      mpu.readGyroscopeMaster(),
      mpu.readMagnetometerMaster()
    ]

    mpu_sample = json.dumps(sample)

    print(mpu_sample)

    time.sleep(0.1)

def start_sampling_imu(mpu_sample):
  Thread(target=continuous_imu_sample, args=[mpu_sample]).start() # does this thread die when parent dies?
