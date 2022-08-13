import subprocess

imu_awake = False

def scan_bus_for_imu():
  subprocess.run(["i2cdetect", "-y", "1"])

# def wake_imu():
#   global imu_awake
#   while (not imu_awake):
#     subprocess.run([])

scan_bus_for_imu()