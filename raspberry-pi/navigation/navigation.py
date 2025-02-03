from threading import Thread

import time
import math

# units are inches and degrees

class Navigation():
  def __init__(self, motion, wide_angle_sensor, narrow_angle_sensor, socket):
    self.socket = socket
    self.robot_length = 14
    self.robot_width = 7.75
    self.robot_height = 9
    self.robot_rotation_width = 20.23
    # imu which is the designed pan/tilt center
    # all sensors aligned except camera (upside down) due to ribbon cable
    self.sensor_height = 7.13
    self.motion = motion
    self.wide_sensor = wide_angle_sensor
    self.narrow_sensor = narrow_angle_sensor
    self.imu_rotation_offset = 2.78 # z-axis (forward)
    self.wide_sensor_y_offest = 0.58 # z-axis
    self.floor_scan_values = []
    self.first_scan = True

    # time: data
    # data includes left_obstacle, right_obstacle
    self.floor_scan_set = {}

    # pan/tilt servo is centered in the beginning of floor scan
    # tilt looks all the way down maximum
    # starts scanning to the right (add), back to midle, starts scanning left
    # next tilt angle, repeat
    # [down angle, [right angle, ra2, ..., max], [left angle, la2, ..., max]]
    # 18" straight ahead is clear level for overhead

    self.floor_scan_positions = [
      [54, [0, 15, 35, 60], [20, 40, 60, 85]],
      [35, [0, 15, 30, 45, 60], [15, 30, 45, 60, 75]],
    ]

    self.scan_min_vals = {
      "54_0_r": 9.13,
      "54_15_r": 9.09,
      "54_35_r": 8.74,
      "54_60_r": 8.42,
      "54_20_l": 9.2,
      "54_40_l": 9.36,
      "54_60_l": 9.09,
      "54_85_l": 8.85,
      "35_0_r": 12.05,
      "35_15_r": 11.66,
      "35_30_r": 11.23,
      "35_45_r": 10.8,
      "35_60_r": 10.53,
      "35_15_l": 12.21,
      "35_30_l": 12.29,
      "35_45_l": 12.29,
      "35_60_l": 11.97,
      "35_75_l": 11.54  
    }

    self.scan_max_vals = {
      "54_0_r": 9.55,
      "54_15_r": 9.52,
      "54_35_r": 9.2,
      "54_60_r": 8.74,
      "54_20_l": 9.71,
      "54_40_l": 9.63,
      "54_60_l": 9.24,
      "54_85_l": 8.97,
      "35_0_r": 12.71,
      "35_15_r": 12.44,
      "35_30_r": 12.05,
      "35_45_r": 11.51,
      "35_60_r": 11.12,
      "35_15_l": 12.71,
      "35_30_l": 12.83,
      "35_45_l": 12.56,
      "35_60_l": 12.17,
      "35_75_l": 11.74  
    }

    '''
    these commands were manually dialed in based on my robot

    turning
    rc_085_085_0895 (turn right 90 deg)
    rc_100_100_0730 (turn left 90 deg)

    move forward
    2.75" (rc_085_098_425)
    10.0" (rc_084_098_1400)
    11.5" (rc_084_098_1550)
    18.5" (rc_084_098_2500)
    '''

  def check_scan_clear(self, key, scan_value):
    if (scan_value >= + self.scan_min_vals[key] and scan_value <= self.scan_max_vals[key]):
      return True

    return False

  def scan_floor(self):
    self.floor_scan_values = []
    scan_time = int(time.time())
    print("")
    self.motion.boot_center()
    time.sleep(2)

    right_obstacle = False
    left_obstacle = False

    for tilt_id, tilt_sample in enumerate(self.floor_scan_positions):
      tilt_angle = tilt_sample[0]
      right_angles = tilt_sample[1]
      left_angles = tilt_sample[2]

      self.motion.tilt("down", tilt_angle)
      time.sleep(1) # wait for vibration to stop

      self.floor_scan_values.append([
        [], # right
        []  # left
      ])

      largest_right = 0

      for right_angle in right_angles:
        self.motion.pan("right", right_angle)
        time.sleep(1)

        sensor_distance = self.wide_sensor.get_distance()

        if (not self.check_scan_clear("{}_{}_r".format(tilt_angle, right_angle), sensor_distance)):
          print("right obstacle")
          right_obstacle = True
          break

        self.floor_scan_values[tilt_id][0].append(sensor_distance)

      self.motion.pan_center()
      time.sleep(2)

      largest_left = 0

      for left_angle in left_angles:
        self.motion.pan("left", left_angle)
        time.sleep(1)

        sensor_distance = self.wide_sensor.get_distance()

        if (not self.check_scan_clear("{}_{}_l".format(tilt_angle, left_angle), sensor_distance)):
          print("left obstacle")
          left_obstacle = True
          break

        self.floor_scan_values[tilt_id][1].append(sensor_distance)

    self.motion.boot_center()
    time.sleep(1)

    self.floor_scan_set[scan_time] = {
      "left_obstacle": left_obstacle,
      "right_obstacle": right_obstacle,
      "scan_data": self.floor_scan_values  
    }

    self.socket.send(self.floor_scan_set[scan_time])

    print(self.floor_scan_set)
    print("")

  # 360
  def full_floor_scan(self):
    for x in range(0, 4):
      self.scan_floor()
      self.socket.send("rc_085_085_0900")

    print(self.floor_scan_values)
    print("")

  def begin_navigation(self):
    # while True:
    if (self.first_scan):
      self.full_floor_scan
    else:
      print("think")

  def start(self):
    Thread(target=self.begin_navigation, args=()).start()