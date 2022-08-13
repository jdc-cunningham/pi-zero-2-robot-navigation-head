# https://stackoverflow.com/questions/45951964/pyinstaller-is-not-recognized-as-internal-or-external-command
# https://stackoverflow.com/questions/41171791/how-to-suppress-or-capture-the-output-of-subprocess-run
# https://stackoverflow.com/questions/7152340/using-a-python-subprocess-call-to-invoke-a-python-script
# https://stackoverflow.com/questions/8713983/python-catching-the-output-from-subprocess-call-with-stdout
# https://stackoverflow.com/questions/48875596/python-run-python-script-as-subprocess-and-get-the-output (works)
# https://stackoverflow.com/questions/24849998/how-to-catch-exception-output-from-python-subprocess-check-output

import subprocess
from subprocess import Popen, PIPE

imu_found = False
imu_awake = False

def imu_on_bus():
  bus_1_scan = subprocess.run(["i2cdetect", "-y", "1"], capture_output=True, text=True)
  return len(bus_1_scan.stderr) == 0 and bus_1_scan.stdout.find("68") > -1

def sample_imu():
  imu_sample = ""

  try:
    return len(subprocess.check_output(["python3", "mpu9250_single.py"]).decode('utf-8').rstrip()) > 10 # 10 is a random number but long enough
  except subprocess.CalledProcessError as e:
    return False # not good

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

  check_count = 0

  if (imu_found):
    while (not imu_awake):
      imu_awake = sample_imu()
      check_count += 1

      if (check_count == max_check and not imu_awake):
        return False
      else:
        return True

print(wake_imu())
