# this applies masks that remove parts of an image so only the stuff
# you care about are highly contrasted for the contour finding
import cv2

# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv

img = cv2.imread('./sample-images/assorted_color_items.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# modifying h between 0-20, 0-100, 0-255 reveals more and more of colors
# HSV x axis S, Y hue
# V is the light range, 0 is dark, 255 is light

# these values are currently manually determined by looking at the graph
# outputs between histogram 1D and 2D
# hsv
mask = cv2.inRange(hsv, (101, 94, 16), (104, 117, 210))
cv2.imwrite('./output-images/mask-applied.jpg', mask)