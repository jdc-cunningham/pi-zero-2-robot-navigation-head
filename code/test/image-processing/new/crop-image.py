# this currently is used for laziness
# but in theory it would be used to parallelize tasks
# https://stackoverflow.com/a/19098258/2710227

import numpy as np
import cv2

def image_dimensions(img_path):
  img = cv2.imread(img_path)
  height, width, channels = img.shape

  return {
    "width": width,
    "height": height
  }

# def image_quads(img):
#   img = cv2.imgread(img_path)
  
print(image_dimensions('./mask-applied.jpg'))