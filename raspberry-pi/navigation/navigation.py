import time

# units are inches and degrees

class Navigation():
  def __init__(self, motion, wide_angle_sensor, narrow_angle_sensor):
    self.robot_length = 14
    self.robot_width = 7.75
    self.robot_height = 9
    self.motion = motion
    self.wide_sensor = wide_angle_sensor
    self.narrow_sensor = narrow_angle_sensor

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

    self.flat_floor_data_sample = [
      [[9.5, 8.93, 8.78, 8.42], [9.09, 9.05, 8.97, 8.74]],
      [[12.5, 11.89, 11.31, 11.0, 10.72], [12.56, 12.32, 11.89, 11.54, 11.31]],
      [[27, 25.74, 22.74, 21.06], [26.56, 25.27, 22.0]]
    ]

    self.floor_scan_values = []

  def scan_floor(self):
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

        sensor_distance = self.narrow_sensor.get_distance() if tilt_angle == 15 else self.wide_sensor.get_distance()

        self.floor_scan_values[tilt_id][0].append(sensor_distance)

      self.motion.pan_center()
      time.sleep(2)

      for left_angle in left_angles:
        self.motion.pan("left", left_angle)
        time.sleep(1)

        sensor_distance = self.narrow_sensor.get_distance() if tilt_angle == 15 else self.wide_sensor.get_distance()

        self.floor_scan_values[tilt_id][1].append(sensor_distance)

    self.motion.boot_center()
    time.sleep(1)

    print(self.floor_scan_values)

  def start(self):
    print('start')