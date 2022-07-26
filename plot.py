'''
This script is a helper script used for plotting our polylines in matplotlib.
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from utils import calculate_arc_center_point
from structs.point import Point

import math

# Line colours of the main, inner, and outer subplots
COLORS = ( 'black', 'red', 'green' )

def plot(polylines):
  vertices, codes = _determine_vertices_and_codes(polylines)
  if len(vertices) != len(codes): return
  fig, ax = plt.subplots()
  for cur_vertices, cur_codes, cur_color in zip(vertices, codes, COLORS):
    path  = Path(cur_vertices, cur_codes)
    patch = patches.PathPatch(path, fill=False, color=cur_color, lw=2)
    ax.add_patch(patch)
  ax.set_xlim(-2, 8)
  ax.set_ylim(-2, 8)
  plt.show()

def _determine_vertices_and_codes(polylines):
  if len(polylines) < 1: return
  vertices, codes = [], []
  for polyline in polylines:
    if len(polyline.segments) < 1: return
    cur_vertices, cur_codes  = [], []
    previous_segment = polyline.segments[0]
    for segment in polyline.segments:
      if previous_segment.end_point != segment.start_point:
        # Line is not connected, move to new start point.
        cur_vertices.append((segment.start_point.x, segment.start_point.y))
        cur_codes.append(Path.MOVETO)
      if segment.is_line():
        # It's a line, draw a simple path.
        cur_vertices.append((segment.end_point.x, segment.end_point.y))
        cur_codes.append(Path.LINETO)
      else:
        # It's an arc, approximate it with a cubic bezier curve.
        # There are three vertices associated with a bezier curve.
        # Add the three points and three codes
        bez_point_1, bez_point_2 = _determine_cubic_bezier_curve_points(segment)
        cur_vertices.extend( [ (bez_point_1.x,       bez_point_1.y),
                               (bez_point_2.x,       bez_point_2.y),
                               (segment.end_point.x, segment.end_point.y), ] )
        cur_codes.extend( [ Path.CURVE4, Path.CURVE4, Path.CURVE4 ] )
      previous_segment = segment
    vertices.append(cur_vertices)
    codes.append(cur_codes)
  return vertices, codes

def _determine_cubic_bezier_curve_points(s):
  start_x, start_y = s.start_point.x, s.start_point.y
  end_x, end_y     = s.end_point.x, s.end_point.y
  xc, yc           = calculate_arc_center_point(s)
  ax = start_x - xc
  ay = start_y - yc
  bx = end_x - xc
  by = end_y - yc
  q1 = ax**2 + ay**2
  q2 = q1 + ax * bx + ay * by
  k2 = (4/3) * (math.sqrt(2 * q1 * q2) - q2) / (ax * by - ay * bx) if (ax * by - ay * bx) != 0 else 1 # workaround
  x2 = xc + ax - k2 * ay
  y2 = yc + ay + k2 * ax
  x3 = xc + bx + k2 * by                                 
  y3 = yc + by - k2 * bx
  return Point(x2, y2), Point(x3, y3)