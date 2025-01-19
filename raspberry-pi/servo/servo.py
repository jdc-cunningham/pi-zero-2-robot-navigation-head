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

  def pan_center(self):
    self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos)

  def pan(self, direction, degree):
    if (direction == "right"):
      # these are not proportional to the #### position above, manually dialed in using external reference (compass)
      right_deg_pos = {
        15: 125,
        20: 225,
        30: 300  
      }
      if (degree == 15):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 125)
      if (degree == 20):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 225)
      if (degree == 30):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 300)
      if (degree == 35):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 350)
      if (degree == 40):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 425)
      if (degree == 45):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 475)
      if (degree == 60):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 600)
    else:
      if (degree == 15):
        self.pigpio.set_servo_pulsewidth(self.pan_servo_pin, self.pan_servo_center_pos - 125)

  def tilt_center(self):
    self.pigpio.set_servo_pulsewidth(self.tilt_servo_pin, self.tilt_servo_center_pos)
