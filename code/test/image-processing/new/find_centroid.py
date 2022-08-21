# https://java2blog.com/cv2-threshold-python/ info on cv2.threshold parameters

import cv2
import math
from operator import itemgetter

# img_path = './crop.jpg'
img_path = './quad1.jpg'

# def find_centroid():

# start, end - x,y tuple
def get_rect_center(start, end):
  print(start[0], start[1])
  print(end[0], end[1])
  top_left = math.floor((end[0] + start[0]) / 2)
  bottom_right = math.floor((end[1] + start[1]) / 2)

  print(top_left)
  print(bottom_right)

  return (
    (top_left-1, bottom_right-1),
    (top_left+1, bottom_right+1)
  )

im = cv2.imread(img_path)
imCopy = im.copy()
imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,0,255,1)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
  if i['area'] < 1000: # consider max as width * height
    continue
  print(i['area'])
  r = cv2.boundingRect(contours[i['cindex']])
  cv2.rectangle(imCopy, (r[0],r[1]), (r[0] + r[2], r[1] + r[3]), (0,0,255), 3)
  centroid = get_rect_center((r[0],r[1]), (r[0] + r[2], r[1] + r[3]))
  cv2.rectangle(imCopy, centroid[0], centroid[1], (0, 255, 0), 3)

# crop set performs better
# imS = cv2.resize(imCopy, (1232, 1640)) # full
imS = cv2.resize(imCopy, (616, 820))

# entire image
# imS = cv2.resize(imCopy, (3280, 2464))
# imS = cv2.resize(imCopy, (820, 616))

cv2.imwrite("./centroid.jpg", imS)
cv2.imshow("big contour boi", imS)
cv2.waitKey(0)