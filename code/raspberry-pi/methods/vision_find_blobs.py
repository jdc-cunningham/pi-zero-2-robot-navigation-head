import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

base_path = os.getcwd()

def get_hsv_v_range(img):
  counts, bins, bars = plt.hist(img.ravel(), 256, [0, 256])

  min = None
  max = None

  for x in range(0, 255, 1):
    if (counts[x] > 0 and min == None):
      min = x
    if (counts[x] > 0 and x < 256):
      max = x
  
  return [min, max]

def get_hsv_hs_range(img):
  


img = cv2.imread(base_path + '/panorama/pan_crop_output.jpg', 0)

get_hsv_v_range(img)
