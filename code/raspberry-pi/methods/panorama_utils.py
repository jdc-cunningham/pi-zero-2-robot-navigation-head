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

def check_for_red(x):
  rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  height, width, channels = rgb_img.shape
  min_red_range = [99, 8, 8]
  max_red_range = [152, 48, 49]

  red_pxs = []

  for y in range(0, int(height * 0.5), 1):
    if (
      pixel_in_range(rgb_img[y, x], min_red_range, max_red_range)
    ):
      red_pxs.append([x, y])

  return red_pxs

# p1, p2 are arrays [x, y]
# orientation/direction depends on which side of the image (left/right)
def get_slope_intercept_info(p1, p2):
  m = (p2[1] - p1[1]) / (p2[0] - p1[0])
  b = p1[1] - (m * p1[0])

  return [round(m, 2), int(b)]

# here you're equating two linear equations together
# ex. -0.78x + 723 = 0.88x - 1147 solving for x
def get_intersection(slope_info_1, slope_info_2):
  b_sum = 0
  x_sum = 0

  if (slope_info_2[1] < 0):
    b_sum = slope_info_1[1] + (-1 * slope_info_2[1])
  else:
    b_sum = slope_info_1[1] - slope_info_2[1]

  if (slope_info_1[0] < 0):
    x_sum = slope_info_2[0] + (-1 * slope_info_1[0])
  else:
    x_sum = slope_info_2[0] - slope_info_1[0]

  x = int(b_sum / x_sum)

  return [x, int((slope_info_1[0] * x) + slope_info_1[1])]

# points: array of [x, y] arrays where red range was detected
# finds and groups pixels by 3 nearest, keeps middle, only 2 points allowed
# eg. y intercept of two lines
def get_line_points(points):
  x = points[0][0]
  y_avg_points = []
  y_set = []

  # print(points)

  for point in points:
    y_set_len = len(y_set)

    if (y_set_len == 0):
      y_set.append(point[1])
    else:
      y_set_last = y_set[y_set_len - 1]

      if (y_set_last + 1 == point[1]):
        y_set.append(point[1])
        y_set_len = len(y_set)

        if (y_set_len == 3):
          y_avg_points.append(y_set[1])
          y_set = []
      else:
        y_set = [point[1]]

  if (len(y_avg_points) == 2):
    return [
      [x, y_avg_points[0]],
      [x, y_avg_points[1]]
    ]
  else:
    return []

def get_camera_center_px():
  # iterate top-left to right, horizontally with vertical slices
  # every 50 pixels from 30% left and 50% max pano img height
  height, width, channels = img.shape
  left_x = int(width * 0.3)

  red_pxs = []

  y_intercept_1 = []
  y_intercept_2 = []

  for x in range (left_x, int(width * 0.7), 50):
    pxs = check_for_red(x)

    if (pxs and len(pxs) >= 6):
      red_pxs.append(pxs)
      
      y_intercepts = get_line_points(pxs)

      # print(y_intercepts)

      if (len(y_intercepts) == 2):
        if (len(y_intercept_1) == 0):
          y_intercept_1 = y_intercepts
        else:
          y_intercept_2 = y_intercepts
          break


  if (len(y_intercept_1) > 0 and len(y_intercept_2) > 0):
    # get slope from line points
    slope_1 = get_slope_intercept_info(
      [y_intercept_1[0][0], y_intercept_1[0][1]],
      [y_intercept_2[0][0], y_intercept_2[0][1]]
    )

    slope_2 = get_slope_intercept_info(
      [y_intercept_1[1][0], y_intercept_1[1][1]],
      [y_intercept_2[1][0], y_intercept_2[1][1]]
    )

    intersection = get_intersection(slope_1, slope_2)

    print(intersection)
  else:
    return [] # failed


get_camera_center_px()
