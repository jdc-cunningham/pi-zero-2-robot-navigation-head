# https://www.teachmemicro.com/raspberry-pi-pwm-servo-tutorial/

import os
import pigpio
import time
import cv2

pi = pigpio.pi()
pan_servo = 12
tilt_servo = 13 

def center_servos():
  pi.set_servo_pulsewidth(pan_servo, 1460)
  pi.set_servo_pulsewidth(tilt_servo, 1340)

def move_servo(which_servo, start_ms, end_ms):
  iter_sign = -5 if (start_ms > end_ms) else 5

  for pw in range(start_ms, end_ms, iter_sign):
    pi.set_servo_pulsewidth(which_servo, pw)
    time.sleep(0.02)

def take_photo(name):
  os.system(f"libcamera-still --rotation 180 -o panorama/{name}.jpg --width 1640 --height 1232 --mode 1640:1232")

def take_photos():
  center_servos()
  time.sleep(2)

  # the tilt does not look up beyond center
  # tilt: 650, 950, 1290
  # pan: 1960, 1460, 960

  # take top/level photos
  pi.set_servo_pulsewidth(pan_servo, 1960) # look left
  time.sleep(2)
  take_photo('left_top')
  pi.set_servo_pulsewidth(pan_servo, 1460)
  time.sleep(2)
  take_photo('center_top')
  pi.set_servo_pulsewidth(pan_servo, 960)
  time.sleep(2)
  take_photo('right_top')
  time.sleep(2)

  # take bottom/level photos
  pi.set_servo_pulsewidth(tilt_servo, 950)
  time.sleep(2)
  take_photo('right_bottom')
  pi.set_servo_pulsewidth(pan_servo, 1460)
  time.sleep(2)
  take_photo('center_bottom')
  pi.set_servo_pulsewidth(pan_servo, 1960)
  time.sleep(2)
  take_photo('left_bottom')

  # recenter
  pi.set_servo_pulsewidth(tilt_servo, 1340)
  pi.set_servo_pulsewidth(pan_servo, 1460)

# modify images due to camera moving
def mod_img(which_img, img):
  if (which_img == 'lt'):
    crop_img = img[0:1232,0:775]
    resz_img = cv2.resize(crop_img, (0, 0), fx=1.18, fy=1.18)
    cut_top_img = resz_img[218:1450, 0:775]
    # height, width, channels = cut_top_img.shape
    # print(height)
    return cut_top_img
  elif (which_img == 'rt'):
    crop_img = img[0:1232,775:1640]
    resz_img = cv2.resize(crop_img, (0, 0), fx=1.18, fy=1.18)
    cut_top_img = resz_img[72:1304, 0:775]
    return cut_top_img
  else:
    return img


def generate_panorama():
  top_imgs = ['panorama/left_top.jpg', 'panorama/center_top.jpg', 'panorama/right_top.jpg']
  mid_imgs = ['panorama/left_middle.jpg', 'panorama/center_middle.jpg', 'panorama/right_middle.jpg']
  bot_imgs = ['panorama/left_bottom.jpg', 'panorama/center_bottom.jpg', 'panorama/right_bottom.jpg']

  # resize to 50%

  tl_img = cv2.imread(top_imgs[0])
  tm_img = cv2.imread(top_imgs[1])
  tr_img = cv2.imread(top_imgs[2])

  # https://stackoverflow.com/a/18767569/2710227
  tl_img = cv2.resize(tl_img, (0, 0), fx=0.5, fy=0.5)
  tm_img = cv2.resize(tm_img, (0, 0), fx=0.5, fy=0.5)
  tr_img = cv2.resize(tr_img, (0, 0), fx=0.5, fy=0.5)

  h_img = cv2.hconcat([mod_img('lt', tl_img), tm_img, mod_img('rt', tr_img)])
  cv2.imwrite('panorama/top.jpg', h_img)

  # free memory?
  tl_img = None
  tm_img = None
  tr_img = None
  h_img = None

  ml_img = cv2.imread(mid_imgs[0])
  mm_img = cv2.imread(mid_imgs[1])
  mr_img = cv2.imread(mid_imgs[2])

  ml_img = cv2.resize(ml_img, (0, 0), fx=0.5, fy=0.5)
  mm_img = cv2.resize(mm_img, (0, 0), fx=0.5, fy=0.5)
  mr_img = cv2.resize(mr_img, (0, 0), fx=0.5, fy=0.5)

  h_img = cv2.hconcat([ml_img, mm_img, mr_img])
  cv2.imwrite('panorama/middle.jpg', h_img)

  ml_img = None
  mm_img = None
  mr_img = None
  h_img = None

  bl_img = cv2.imread(bot_imgs[0])
  bm_img = cv2.imread(bot_imgs[1])
  bb_img = cv2.imread(bot_imgs[2])

  bl_img = cv2.resize(bl_img, (0, 0), fx=0.5, fy=0.5)
  bm_img = cv2.resize(bm_img, (0, 0), fx=0.5, fy=0.5)
  bb_img = cv2.resize(bb_img, (0, 0), fx=0.5, fy=0.5)

  h_img = cv2.hconcat([bl_img, bm_img, bb_img])
  cv2.imwrite('panorama/bot.jpg', h_img)

# def gen_panorama():
