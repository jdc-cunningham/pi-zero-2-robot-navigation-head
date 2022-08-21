import cv2
import numpy as np

img = cv2.imread('./test-mr.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# range I picked didn't work
# mask = cv2.inRange(hsv, (0, 0, 0), (179, 0, 255))
# cv2.imwrite('./mask-applied.jpg', mask)

# https://stackoverflow.com/a/55710477/2710227
# hmm not very good it thinks green is black
lower_gray = np.array([0, 5, 50], np.uint8)
upper_gray = np.array([179, 50, 255], np.uint8)
mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
img_res = cv2.bitwise_and(img, img, mask = mask_gray)
cv2.imwrite('./mask-applied.jpg', img_res)