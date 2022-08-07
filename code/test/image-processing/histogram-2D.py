# this generates a plot that provides the H and S values
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('./sample-images/assorted_color_items.jpg')
hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
hist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

plt.imshow(hist, interpolation = 'nearest')
plt.show()

# x axis shows S values, Y show Hue
# https://docs.opencv.org/master/dd/d0d/tutorial_py_2d_histogram.html

# values returned max bounds:
# x, S: 12, 166
# y, H: 50, 106s