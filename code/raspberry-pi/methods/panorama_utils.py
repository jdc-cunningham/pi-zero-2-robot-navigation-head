import os
import cv2

base_path = os.getcwd()
img = cv2.imread(base_path + '/panorama/pan_crop_output_crosshair.jpg')

def run():
  rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  print(rgb_img[465, 1191]) # BGR

def peek_crop():
  crop_img = img[464:466,1190:1192]
  peek_crop_out_path = base_path + '/panorama/peek_crop.jpg'
  cv2.imwrite(peek_crop_out_path, crop_img)

def iterate_samples():
  sliver_sample = cv2.imread(base_path + '/panorama/red-sliver.jpg')
  rgb_sliver_sample = cv2.cvtColor(sliver_sample, cv2.COLOR_BGR2RGB)
  center_sample = cv2.imread(base_path + '/panorama/red-center.jpg')
  rgb_center_sample = cv2.cvtColor(center_sample, cv2.COLOR_BGR2RGB)

  # height, width, channels = rgb_sliver_sample.shape
  height, width, channels = rgb_center_sample.shape

  print(width, height)

  for x in range(0, width, 1):
    for y in range(0, height, 1):
      # output to array for JS html/css vis conf of colors
      # print(",".join(str(rgb_sliver_sample[y, x]).split("  ")) + ",")
      print(",".join(str(rgb_center_sample[y, x]).split("  ")) + ",")

iterate_samples()
