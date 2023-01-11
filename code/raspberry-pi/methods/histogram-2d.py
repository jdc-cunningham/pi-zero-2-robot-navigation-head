# this generates a plot that provides the H and S values
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

base_path = os.getcwd()
img = cv2.imread(base_path + '/panorama/pan_crop_output_crosshair.jpg')
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

plt.imshow(hist, interpolation = 'nearest')
plt.show()

# x axis shows S values, Y show Hue
# https://docs.opencv.org/master/dd/d0d/tutorial_py_2d_histogram.html

# values returned max bounds:
# x, S: 12, 166
# y, H: 50, 106s