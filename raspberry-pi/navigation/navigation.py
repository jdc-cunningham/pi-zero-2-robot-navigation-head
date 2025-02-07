from threading import Thread

import time
import json

# units are inches and degrees

class Navigation():
  def __init__(self, motion, wide_angle_sensor, narrow_angle_sensor, vehicle_socket, web_ui_socket):
    self.vehicle_socket = vehicle_socket
    self.web_ui_socket = web_ui_socket
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
    self.x_offset = 0 # left or right
    self.y_offset = 0 # up or down

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
      "54_0_r": 9.0,
      "54_15_r": 9.9,
      "54_35_r": 8.75,
      "54_60_r": 8.25,
      "54_20_l": 9.25,
      "54_40_l": 9.0,
      "54_60_l": 9.0,
      "54_85_l": 8.75,
      "35_0_r": 11.75,
      "35_15_r": 11.5,
      "35_30_r": 11.0,
      "35_45_r": 10.5,
      "35_60_r": 10.25,
      "35_15_l": 12.25,
      "35_30_l": 12.25,
      "35_45_l": 12.0,
      "35_60_l": 11.75,
      "35_75_l": 11.5
    }

    self.scan_max_vals = {
      "54_0_r": 10,
      "54_15_r": 10.9,
      "54_35_r": 9.75,
      "54_60_r": 9.25,
      "54_20_l": 10.25,
      "54_40_l": 10,
      "54_60_l": 10,
      "54_85_l": 9.75,
      "35_0_r": 12.75,
      "35_15_r": 12.5,
      "35_30_r": 12,
      "35_45_r": 11.5,
      "35_60_r": 11.25,
      "35_15_l": 13.25,
      "35_30_l": 13.25,
      "35_45_l": 13,
      "35_60_l": 12.75,
      "35_75_l": 12.5
    }

    '''
    these commands were manually dialed in based on my robot

    turning
    rc_085_085_0895 (turn right 90 deg)
    rc_100_100_0730 (turn left 90 deg)

    move forward
    sensor is 3.64 inches ahead of wheel axle
    2.75" (rc_085_098_425)
    6.36" (rc_084_098_0850)
    8.00" (rc_084_098_1050)
    10.0" (rc_084_098_1400)
    11.5" (rc_084_098_1550)
    18.5" (rc_084_098_2500)
    '''

  def check_scan_clear(self, key, scan_value):
    if (scan_value >= + self.scan_min_vals[key] and scan_value <= self.scan_max_vals[key]):
      return True

    print("{}-{}".format(self.scan_min_vals[key], self.scan_max_vals[key]))

    return False

  def scan_floor(self, scan_dir):
    self.client_send_msg("telemetry", "scanning floor")

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
        print("right {}_{} {}".format(tilt_angle, right_angle, sensor_distance))

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
        print("left obstacle, {}_{} {}".format(tilt_angle, left_angle, sensor_distance))

        if (not self.check_scan_clear("{}_{}_l".format(tilt_angle, left_angle), sensor_distance)):
          print("left obstacle")
          left_obstacle = True
          break

        self.floor_scan_values[tilt_id][1].append(sensor_distance)

    self.motion.boot_center()
    time.sleep(1)

    self.floor_scan_set[scan_time] = {
      "type": "scan_data",
      "direction": scan_dir,
      "left_obstacle": left_obstacle,
      "right_obstacle": right_obstacle,
      "scan_time": scan_time,
      "x_offset": self.x_offset,
      "y_offset": self.y_offset
    }

    self.client_send_msg("scan_data", self.floor_scan_set[scan_time])

    print("")

  def client_send_msg(self, msg_type, msg):
    self.web_ui_socket.send(json.dumps({
      "type": msg_type,
      "msg": msg
    }))

  # 360
  def full_floor_scan(self):
    angle = 0

    for x in range(0, 4):
      self.scan_floor(angle)
      angle += 90

      self.client_send_msg("telemetry", "turning to {}".format(angle))
      self.vehicle_socket.send("rc_085_085_0900")

  def move_forward(self, distance):
    self.y_offset += distance
    self.client_send_msg("telemetry", "moving forward {} inches".format(distance))
    time.sleep(1)
    self.vehicle_socket.send("rc_084_098_1050")

  def begin_navigation(self):
    # while True:
    if (self.first_scan):
      # self.full_floor_scan()
      # self.move_forward(8)
      self.scan_floor(0)
    else:
      print("think")

  def start(self):
    Thread(target=self.begin_navigation, args=()).start()