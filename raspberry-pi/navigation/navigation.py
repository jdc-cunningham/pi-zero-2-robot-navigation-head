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
    self.floor_scan_set = {} # time: data

    # pan/tilt servo is centered in the beginning of floor scan
    # tilt looks all the way down maximum
    # starts scanning to the right (add), back to midle, starts scanning left
    # next tilt angle, repeat
    # [down angle, [right angle, ra2, ..., max], [left angle, la2, ..., max]]
    # 18" straight ahead is clear level for overhead

    self.floor_scan_positions = [
      [54, [0, 15, 35, 60], [20, 40, 60, 85]],
      [35, [0, 15, 30, 45, 60], [15, 30, 45, 60, 75]],
      [15, [0, 20, 40, 60], [20, 40, 60]]
    ]

    '''
    these commands were manually dialed in based on my robot

    turning
    rc_085_085_0895 (turn right 90 deg)
    rc_100_100_0730 (turn left 90 deg)

    move forward
    2.75" (rc_085_098_425)
    11.5" (rc_084_098_1550)
    18.5" (rc_084_098_2500)
    '''

  def scan_floor(self):
    print("")
    self.motion.boot_center()
    time.sleep(2)

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

      for right_angle in right_angles:
        self.motion.pan("right", right_angle)
        time.sleep(1)

        # sensor_distance = self.narrow_sensor.get_distance() if tilt_angle == 15 else self.wide_sensor.get_distance()
        sensor_distance = self.wide_sensor.get_distance()

        self.floor_scan_values[tilt_id][0].append(sensor_distance)

      self.motion.pan_center()
      time.sleep(2)

      for left_angle in left_angles:
        self.motion.pan("left", left_angle)
        time.sleep(1)

        # sensor_distance = self.narrow_sensor.get_distance() if tilt_angle == 15 else self.wide_sensor.get_distance()
        sensor_distance = self.wide_sensor.get_distance()

        self.floor_scan_values[tilt_id][1].append(sensor_distance)

    self.motion.boot_center()
    time.sleep(1)

    print(self.floor_scan_values)
    print("")

  # 360
  def full_floor_scan(self):
    for x in range(0, 4):
      self.scan_floor()
      self.socket.send("rc_085_085_0900")
      self.floor_scan_set[math.floor(time.time())] = self.floor_scan_values
      self.floor_scan_values = []

    print(self.floor_scan_values)
    print("")

  def start(self):
    print('start')