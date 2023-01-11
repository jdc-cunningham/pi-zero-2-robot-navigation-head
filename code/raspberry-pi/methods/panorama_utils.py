import os
import cv2

base_path = os.getcwd()

def run():
  img = cv2.imread(base_path + '/panorama/pan_crop_output_crosshair.jpg')
  rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  print(rgb_img[1193, 466]) # BGR

def crop():
  # do cropping
