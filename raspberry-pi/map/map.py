# this is a 2D map
from matplotlib.patches import Rectangle

import matplotlib.pyplot as plot

class Map():
  def __init__(self):
    self.robot_pos = [0, 0]
    '''
      {
        "angle": 0,
        "x_offset": 0,
        "y_offset": 0,
        "width": 0,
        "distance": 0,
        "time": 0
      }
    '''
    self.scans = [
      {
        "angle": 0,
        "x_offset": 1,
        "y_offset": 1,
        "width": 2,
        "distance": 2,
        "time": 0
      }
    ]

  # https://stackoverflow.com/questions/13013781/how-to-draw-a-rectangle-over-a-specific-region-in-a-matplotlib-graph
  # this code is not ran on a headless raspberry pi it is to be ran on the host computer/one with a GUI
  def plot_map(self):
    fig = plot.figure()

    plot.xlim(0, 10)
    plot.ylim(0, 10)
    current_axis = plot.gca()

    for scan in self.scans:
      current_axis.add_patch(Rectangle((scan["x_offset"], scan["y_offset"]), scan["width"], scan["distance"], facecolor="blue"))

    plot.show()
