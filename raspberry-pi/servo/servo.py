import pigpio

class Servo:
  def __init__(self):
    self.pigpio = pigpio.pi()
    self.pan_servo_pin = 12
    self.pan_servo_pos = 1200
    self.pan_servo_center_pos = 1450  # 1500 midpoint, 2500 max
    self.tilt_servo_pin = 13
    self.tilt_servo_pos = 1200
    self.tilt_servo_center_pos = 1200

  def boot_center(self):
    self.pigpio.set_servo_pulsewidth(self.tilt_servo_pin, self.tilt_servo_center_pos)
    self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos)

  def pan(self, direction, degree):
    if (direction == "right"):
      # these are not proportional to the #### position above, manually dialed in using external reference (compass)
      right_deg_pos = {
        0: 0,
        15: 125,
        20: 225,
        30: 300,
        35: 350,
        40: 425,
        45: 475,
        60: 600,
        15: 125
      }

      self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - right_deg_pos[degree])
    else:
      left_deg_pos = {
        0: 0,
        15: 200,
        20: 250,
        30: 360,
        40: 450,
        45: 500,
        60: 650,
        75: 800,
        85: 900
      }

      self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos + left_deg_pos[degree])

  def pan_center(self):
    self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos)

  def tilt(self, direction, degree):
    tilt_deg_pos = {
      15: 50,
      35: 275,
      54: 400
    }

    if (direction == "down"):
      self.pigpio.set_servo_pulsewidth(self.tilt_servo_pin, self.tilt_servo_center_pos - tilt_deg_pos[degree])

  def tilt_center(self, degree):
    self.pigpio.set_servo_pulsewidth(self.tilt_servo_pin, self.tilt_servo_center_pos)
