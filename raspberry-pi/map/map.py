# this is a 2D map
from dataclasses import dataclass
from matplotlib.patches import Polygon

import matplotlib.pyplot as plot
import math

class Map():
  def __init__(self):
    self.robot_pos = [0, 0]

    self.scans = [
    ]

  def deg_to_rad(self, deg):
    return deg * 0.0175

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

  @dataclass
  class ScanPlane():
    angle: float
    x_offset: float
    y_offset: float
    width: float
    distance: float
    time: float

  # this code is not ran on a headless raspberry pi it is to be ran on the host computer/one with a GUI
  # https://stackoverflow.com/questions/13013781/how-to-draw-a-rectangle-over-a-specific-region-in-a-matplotlib-graph
  # https://stackoverflow.com/a/43971350
  # https://stackoverflow.com/a/68532480
  def plot_map(self):
    plot.figure()
    plot.xlim(-10, 10)
    plot.ylim(-10, 10)
    current_axis = plot.gca()

    scan_plane = self.ScanPlane(0.0, 1.0, 1.0, 2.0, 3.0, 0.0)
    sp_vertices = self.get_plane_vertices(scan_plane)
    sp_polygon = Polygon(sp_vertices)
    rotated_plane = self.rotate_plane(90, sp_vertices)

    current_axis.add_patch(sp_polygon)

    print(rotated_plane)

    polygon = Polygon(rotated_plane)

    current_axis.add_patch(polygon)
    plot.gca().set_aspect('equal') # square ar
    plot.show()
