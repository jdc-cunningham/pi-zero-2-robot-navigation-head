# this is a 2D map
from dataclasses import dataclass
from matplotlib.patches import Rectangle

import matplotlib.pyplot as plot

class Map():
  def __init__(self):
    self.robot_pos = [0, 0]

    self.scans = [
    ]

  def get_plane_vertices(self, plane):
    return [
      [plane.x_offset,  plane.y_offset],
      [plane.x_offset, plane.y_offset + plane.distance],
      [plane.x_offset + plane.width, plane.y_offset],
      [plane.x_offset + plane.width, plane.y_offset + plane.distance]
    ]

  # counter-clockwise is positive
  # https://academo.org/demos/rotation-about-point/
  def rotate_plane(self, angle, plane_vertices):
    for plane_vertice in plane_vertices:
      # consider what quadrant the point is in, direction of turning for signage
      print(plane_vertice)

  @dataclass
  class ScanPlane():
    angle: float
    x_offset: float
    y_offset: float
    width: float
    distance: float
    time: float

  # https://stackoverflow.com/questions/13013781/how-to-draw-a-rectangle-over-a-specific-region-in-a-matplotlib-graph
  # this code is not ran on a headless raspberry pi it is to be ran on the host computer/one with a GUI
  def plot_map(self):
    fig = plot.figure()

    plot.xlim(0, 10)
    plot.ylim(0, 10)
    current_axis = plot.gca()

    scan_plane = self.ScanPlane(0.0, 1.0, 1.0, 2.0, 3.0, 0.0)

    current_axis.add_patch(
      Rectangle(
        (scan_plane.x_offset, scan_plane.y_offset),
        scan_plane.width,
        scan_plane.distance, 
        facecolor="blue"
      )
    )

    plot.show()
