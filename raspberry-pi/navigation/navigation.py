# units are inches and degrees

class Navigation():
  def __init__(self):
    self.robot_length = 14
    self.robot_width = 7.75
    self.robot_height = 9

    # pan/tilt servo is centered in the beginning of floor scan
    # tilt looks all the way down maximum
    # starts scanning to the right (add), back to midle, starts scanning left
    # next tilt angle, repeat
    # [down angle, [right angle, ra2, ..., max], [left angle, la2, ..., max]]
    # 18" straight ahead is clear level for overhead
    self.floor_scan_positions = [
      [54, [15, 35, 60], [20, 40, 60, 85]],
      [35, [15, 30, 45, 60], [15, 30, 45, 60, 75]],
      [15, [20, 40, 60], [20, 40, 60]]
    ]

  def scan_floor(self):
    print('start')

  def start(self):
    print('start')