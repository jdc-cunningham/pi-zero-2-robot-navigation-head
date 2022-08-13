# https://stackoverflow.com/questions/45951964/pyinstaller-is-not-recognized-as-internal-or-external-command
# https://stackoverflow.com/questions/41171791/how-to-suppress-or-capture-the-output-of-subprocess-run
# https://stackoverflow.com/questions/7152340/using-a-python-subprocess-call-to-invoke-a-python-script

import subprocess
from subprocess import Popen, PIPE

imu_found = False
imu_awake = False

def imu_on_bus():
  bus_1_scan = subprocess.run(["i2cdetect", "-y", "1"], capture_output=True, text=True)
  return len(bus_1_scan.stderr) == 0 and bus_1_scan.stdout.find("68") > -1

def sample_imu():
  print("pre sample")
  imu_sample = subprocess.Popen(["python3", "mpu9250.py"])
  print("post sample")
  print(imu_sample.communcate())

def wake_imu():
  global imu_awake, imu_found

  max_check = 5
  check_count = 0

  while (not imu_found):
    imu_found = imu_on_bus()
    check_count += 1
    
    if (not imu_found and check_count == max_check):
      print("failed to find imu")
      break

  if (imu_found):
    sample_imu()

wake_imu()
