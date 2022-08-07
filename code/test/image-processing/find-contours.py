# here you can find the contours if any and iterate through them
# by size and can specify minimum areas to care for
import time
import numpy as np
import cv2
from operator import itemgetter
import json

im = cv2.imread('./output-images/mask-applied.jpg')
imCopy = im.copy()
imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy =  cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imCopy,contours,-1,(255,0,0), 1) # working, shows too many

largest_contour_index = 0
largest_area = 0
areas_and_contour_indexes = []

for i in range(len(contours)):
  a = cv2.contourArea(contours[i], False) #  Find the area of contour
  areas_and_contour_indexes.append({
    "area": a,
    "cindex": i
  })
  if a > largest_area:
    largest_area = a
    largest_contour_index = i;                # Store the index of largest contour

# sort by descending area size
bounded_contours = sorted(areas_and_contour_indexes, key=itemgetter('area'))
loop_counter = -1

for i in reversed(bounded_contours):
  loop_counter += 1
  if loop_counter == 0:
    continue
  if i['area'] < 1000:
    continue
  print i['area']
  r = cv2.boundingRect(contours[i['cindex']])
  cv2.rectangle(imCopy, (r[0],r[1]), (r[0] + r[2], r[1] + r[3]), (0,0,255), 3)

imS = cv2.resize(imCopy, (960, 540))
cv2.imshow("big contour boi", imS)
cv2.waitKey(0)