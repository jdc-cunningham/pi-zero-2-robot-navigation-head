# this is a 2D map
from dataclasses import dataclass
from matplotlib.patches import Polygon

import matplotlib.pyplot as plot
import math
import time

class Map():
  def __init__(self):
    self.robot_pos = [0, 0]

    # right set, then left
    self.full_floor_scan_planes = []
    self.scans = []
    self.init_floor_scan_planes(0, 0, 0, int(time.time()))
  
  @dataclass
  class ScanPlane():
    angle: float
    x_offset: float
    y_offset: float
    width: float
    distance: float
    time: int

  def init_floor_scan_planes(self, angle, offset_x, offset_y, time):
    # these angles match the tilt angles in navigation.py
    right_54 = self.ScanPlane(angle, offset_x, offset_y,        8,     3.84, time)
    right_35 = self.ScanPlane(angle, offset_x, offset_y + 3.84, 15.89, 7.04, time)
    left_54 =  self.ScanPlane(angle, offset_x, offset_y,        -8,     3.84, time)
    left_35 =  self.ScanPlane(angle, offset_x, offset_y + 3.84, -15.89, 7.04, time)

    self.full_floor_scan_planes.extend([right_54, right_35, left_54, left_35])

  def deg_to_rad(self, deg):
    return deg * 0.017453

  def get_plane_vertices(self, plane):
    return [
      [plane.x_offset,  plane.y_offset],
      [plane.x_offset + plane.width, plane.y_offset],
      [plane.x_offset + plane.width, plane.y_offset + plane.distance],
      [plane.x_offset, plane.y_offset + plane.distance]
    ]

  # counter-clockwise is positive
  # https://academo.org/demos/rotation-about-point/
  def rotate_plane(self, angle, plane_vertices):
    new_coords = []
    rad = self.deg_to_rad(angle)

    print(plane_vertices)

    for plane_vertice in plane_vertices:
      # consider what quadrant the point is in, direction of turning for signage
      new_coords.append([
        round(
          (plane_vertice[0] * math.cos(rad)) - (plane_vertice[1] * math.sin(rad))
        , 2),
        round(
          (plane_vertice[1] * math.cos(rad)) + (plane_vertice[0] * math.sin(rad))
        , 2)
      ])

    return new_coords

  # this code is not ran on a headless raspberry pi it is to be ran on the host computer/one with a GUI
  # https://stackoverflow.com/questions/13013781/how-to-draw-a-rectangle-over-a-specific-region-in-a-matplotlib-graph
  # https://stackoverflow.com/a/43971350
  # https://stackoverflow.com/a/68532480
  def plot_map(self):
    plot.figure()
    plot.xlim(-50, 50)
    plot.ylim(-50, 50)
    plot.gca().set_aspect('equal') # square ar

    current_axis = plot.gca()

    # scan_plane = self.ScanPlane(0.0, 1.0, 1.0, 2.0, 3.0, 0)
    # sp_vertices = self.get_plane_vertices(scan_plane)
    # sp_polygon = Polygon(sp_vertices)
    # rotated_plane = self.rotate_plane(90, sp_vertices)
    # current_axis.add_patch(sp_polygon)
    # polygon = Polygon(rotated_plane)

    # current_axis.add_patch(polygon)

    for scan_plane in self.full_floor_scan_planes:
      print(scan_plane)
      sp_vertices = self.get_plane_vertices(scan_plane)
      sp_polygon = Polygon(sp_vertices)
      current_axis.add_patch(sp_polygon)

    plot.show()
