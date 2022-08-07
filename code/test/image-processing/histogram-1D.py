# this tells you the available light (V in HSV)
# this is straight up from the docs
# 0 - 255, dark is on left, bright on right
# graph output Y is number of pixels
import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('./sample-images/assorted_color_items.jpg', 0) # grayscale, outputs range between 15, 195

# may have speed gains not using plot to get values from ravel

# https://stackoverflow.com/questions/20128898/get-data-points-from-a-histogram-in-python
counts, bins, bars = plt.hist(img.ravel(), 256, [0, 256])

plt.show()