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
  pi.set_servo_pulsewidth(pan_servo, 1860) # look left + 450
  time.sleep(3)
  take_photo('left_outer_top')
  pi.set_servo_pulsewidth(pan_servo, 1660) # look left + 450
  time.sleep(3)
  take_photo('left_inner_top')
  pi.set_servo_pulsewidth(pan_servo, 1460)
  time.sleep(3)
  take_photo('center_top')
  pi.set_servo_pulsewidth(pan_servo, 1260)
  time.sleep(3)
  take_photo('right_inner_top')
  pi.set_servo_pulsewidth(pan_servo, 1060)
  time.sleep(3)
  take_photo('right_outer_top')
  time.sleep(3)

  # take bottom/level photos
  pi.set_servo_pulsewidth(tilt_servo, 950)
  time.sleep(2)
  take_photo('right_outer_bottom')
  pi.set_servo_pulsewidth(tilt_servo, 1260)
  time.sleep(2)
  take_photo('right_inner_bottom')
  pi.set_servo_pulsewidth(pan_servo, 1460)
  time.sleep(2)
  take_photo('center_bottom')
  pi.set_servo_pulsewidth(pan_servo, 1660)
  time.sleep(2)
  take_photo('left_inner_bottom')
  pi.set_servo_pulsewidth(pan_servo, 1860)
  time.sleep(2)
  take_photo('left_outer_bottom')

  # recenter
  pi.set_servo_pulsewidth(tilt_servo, 1340)
  pi.set_servo_pulsewidth(pan_servo, 1460)

take_photos()

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

def build_panorama(img_paths, out_path):
  imgs = []

  # generate top panorama set
  for i in range(len(img_paths)):
    imgs.append(cv2.imread(img_paths[i]))

  stitchy = cv2.Stitcher.create()
  (dummy,output)=stitchy.stitch(imgs)

  if dummy != cv2.STITCHER_OK:
    # handle this error somehow
    return False
  else:
    cv2.imwrite(out_path, output)
    return True

def gen_panorama():
  base_path = os.getcwd()

  top_img_paths = [
    base_path + '/panorama/left_outer_top.jpg',
    base_path + '/panorama/left_inner_top.jpg',
    base_path + '/panorama/center_top.jpg',
    base_path + '/panorama/right_inner_top.jpg',
    base_path + '/panorama/right_outer_top.jpg'
  ]

  top_out_path = base_path + '/panorama/top_output.jpg'

  print(build_panorama(top_img_paths, top_out_path))

  bot_img_paths = [
    base_path + '/panorama/left_outer_bottom.jpg',
    base_path + '/panorama/left_inner_bottom.jpg',
    base_path + '/panorama/center_bottom.jpg',
    base_path + '/panorama/right_inner_bottom.jpg',
    base_path + '/panorama/right_outer_bottom.jpg'
  ]

  bot_out_path = base_path + '/panorama/bot_output.jpg'

  print(build_panorama(bot_img_paths, bot_out_path))

  # pan_img_paths = [
  #   top_out_path,
  #   bot_out_path
  # ]

  # pan_out_path = base_path + '/panorama/pan_output.jpg'

  # print(build_panorama(pan_img_paths, pan_out_path))

# gen_panorama()