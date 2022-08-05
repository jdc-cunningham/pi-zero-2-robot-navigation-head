# https://raspberrypi.stackexchange.com/questions/106697/tfmini-plus-lidar-not-working

ser = serial.Serial(
  port="/dev/serial0",
  baudrate = 115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

while 1:
  x=ser.readline()
  print(x)