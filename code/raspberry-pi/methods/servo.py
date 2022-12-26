# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import pigpio
import time
import asyncio
import websockets

socket_conn = None
pi = pigpio.pi()
pan_servo = 12
pan_center = 1460

tilt_servo = 13
tilt_center = 1340

# 1500 is midpoint
# 2500 is max

# vertical camera positions
# 1290 vertically centered on wifi-buggy
# 950 mb
# 650 bottom camera pos
# left 1760
# sweep 1460 center
# right 1160
def boot_center():
  pi.set_servo_pulsewidth(pan_servo, pan_center) # > 1500, left -- 1460 center
  pi.set_servo_pulsewidth(tilt_servo, tilt_center) # < 1500 down max 1490 -- 1290 center

def move_servo(which, ms):
  if (which == "pan"):
    pi.set_servo_pulsewidth(pan_servo, ms)
  else:
    pi.set_servo_pulsewidth(tilt_servo, ms)

def tmp_look_around():
  # look left
  for pw in range(1440,1640,5):
    pi.set_servo_pulsewidth(pan_servo, pw)
    # print(pw)
    time.sleep(0.02)

  # look down
  for pw in range(1090,890,-5):
    pi.set_servo_pulsewidth(tilt_servo, pw)
    # print(pw)
    time.sleep(0.02)

  # look up to middle
  for pw in range(890,1090,5):
    pi.set_servo_pulsewidth(tilt_servo, pw)
    # print(pw)
    time.sleep(0.02)

  # look left to middle
  for pw in range(1640,1440,-5):
    pi.set_servo_pulsewidth(pan_servo, pw)
    # print(pw)
    time.sleep(0.02)

def rotate():
  for pw in range(1460,1670,10):
    pi.set_servo_pulsewidth(pan_servo, pw)
    time.sleep(0.01)

# boot_center()
# time.sleep(1)
# rotate()

async def connect():
  async with websockets.connect("ws://192.168.1.195:80") as websocket:
    socket_conn = websocket
    await socket_conn.send("m_r360")
    # await websocket.recv()

def battery_skit():
  # nod
  for run in range(0, 2, 1):
    for pw in range(1390,1090,-10):
      pi.set_servo_pulsewidth(tilt_servo, pw)
      # print(pw)
      time.sleep(0.01)

    for pw in range(1090, 1390, 10):
      pi.set_servo_pulsewidth(tilt_servo, pw)
      time.sleep(0.01)

  time.sleep(3)
  asyncio.run(connect())

def remote_center():
  boot_center()

# track init pos
hPos = pan_center
vPos = tilt_center

def remote_left():
  global hPos

  newPos = hPos + 10

  if (newPos > 2500):
    return

  for pw in range(hPos, newPos, 1):
    pi.set_servo_pulsewidth(pan_servo, pw)
    time.sleep(0.01)

  hPos = newPos

def remote_right():
  global hPos

  newPos = hPos - 10

  if (newPos < 0):
    return

  for pw in range(hPos, newPos, -1):
    pi.set_servo_pulsewidth(pan_servo, pw)
    time.sleep(0.01)

  hPos = newPos

def remote_up():
  global vPos

  newPos = vPos + 10

  if (newPos < 0):
    return

  for pw in range(vPos, newPos, 1):
    pi.set_servo_pulsewidth(tilt_servo, pw)
    time.sleep(0.01)

  vPos = newPos

def remote_down():
  global vPos

  newPos = vPos - 10

  if (newPos > 1490):
    return

  for pw in range(vPos, newPos, -1):
    pi.set_servo_pulsewidth(tilt_servo, pw)
    time.sleep(0.01)

  vPos = newPos

# boot_center()
# time.sleep(1.5)
# battery_skit()

def pan_control(deg):
  # do stuff

def tilt_control(deg):
  # do stuff