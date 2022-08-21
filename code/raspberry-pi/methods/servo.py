# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import pigpio
import time
import asyncio
import websockets

socket_conn = None
pi = pigpio.pi()
pan_servo = 12
tilt_servo = 13

# 1500 is midpoint
# 2500 is max

def boot_center():
  pi.set_servo_pulsewidth(pan_servo, 1460) # > 1500, left
  # pi.set_servo_pulsewidth(tilt_servo, 1090) # < 1500 up max 1490
  pi.set_servo_pulsewidth(tilt_servo, 1390)

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

  asyncio.run(connect())

battery_skit()
