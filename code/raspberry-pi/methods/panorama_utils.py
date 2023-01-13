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

  height, width, channels = rgb_sliver_sample.shape
  # height, width, channels = rgb_center_sample.shape

  print(width, height)

  smallest_r = 255
  smallest_g = 255
  smallest_b = 255

  largest_r = 0
  largest_g = 0
  largest_b = 0

  for x in range(0, width, 1):
    for y in range(0, height, 1):
      # output to array for JS html/css vis conf of colors
      # print(",".join(str(rgb_sliver_sample[y, x]).split("  ")) + ",")
      # print(",".join(str(rgb_center_sample[y, x]).split("  ")) + ",")
      r, g, b = rgb_sliver_sample[y, x]

      smallest_r = r if r < smallest_r else smallest_r
      smallest_g = g if g < smallest_g else smallest_g
      smallest_b = b if b < smallest_b else smallest_b

      largest_r = r if r > largest_r else largest_r
      largest_g = g if g > largest_g else largest_g
      largest_b = b if b > largest_b else largest_b

  print(smallest_r, smallest_g, smallest_b)
  print(largest_r, largest_g, largest_b)

# red color
def pixel_in_range(pixel_rgb, min_pixel_rgb, max_pixel_rgb):
  in_range = True

  for pixel in range(0, 2, 1):
    if (
      pixel_rgb[pixel] < min_pixel_rgb[pixel] or
      pixel_rgb[pixel] > max_pixel_rgb[pixel]
    ):
      in_range = False
      break

  return in_range
      
  

def compare():
  rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  height, width, channels = rgb_img.shape
  left_x = int(width * 0.3)
  print(left_x)
  min_red_range = [99, 8, 8]
  max_red_range = [152, 48, 49]

  red_pixel_found = False

  # for y in range(0, int(height * 0.85), 1):
  #   if (
  #     pixel_in_range(rgb_img[y, left_x], min_red_range, max_red_range)
  #   ):
  #     red_pixel_found = True
  #     print(y)

  for y in range(0, int(height * 0.85), 1):
    if (
      pixel_in_range(rgb_img[y, left_x + 300], min_red_range, max_red_range)
    ):
      red_pixel_found = True
      print(y)

compare()