# this currently is used for laziness
# but in theory it would be used to parallelize tasks
# https://stackoverflow.com/a/19098258/2710227
# https://stackoverflow.com/questions/15589517/how-to-crop-an-image-in-opencv-using-python
# https://www.tutorialspoint.com/python_pillow/python_pillow_cropping_an_image.htm

import numpy as np
import cv2
import math
from PIL import Image

img_path = './mask-applied.jpg'

def image_dimensions(img):
  img = cv2.imread(img_path)
  height, width, channels = img.shape

  return {
    "width": width,
    "height": height
  }

# only in memory
def image_quads(img_path):
  img = cv2.imread(img_path)
  img_dims = image_dimensions(img)
  x = math.floor(img_dims.get('height')/2)
  y = math.floor(img_dims.get('width')/2)
  crop_img = img[x, y]

def image_quads_save(img_path):
  img_dims = image_dimensions(cv2.imread(img_path))
  img = Image.open(img_path)
  og_width = img_dims.get('width')
  og_height = img_dims.get('height')
  midp_x = math.floor(og_width/2)
  midp_y = math.floor(og_height/2)

  quad_dims = [
    (0, 0, midp_x, midp_y),
    (midp_x, 0, og_width, midp_y),
    (0, midp_y, midp_x, og_height),
    (midp_x, midp_y, og_width, og_height)
  ]

  counter = 1;

  for quad_dim in quad_dims:
    cropped_img = img.crop((quad_dim[0], quad_dim[1], quad_dim[2], quad_dim[3]))
    cropped_img.save(f'./quad{counter}.jpg')
    counter += 1

image_quads_save(img_path)