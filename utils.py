import math

from structs.point import Point
from structs.segment import Segment
from structs.polyline import Polyline

# Takes in a polyline and returns a new polyline with parallel segments
# a specified 'd' distance away.
def get_parallels(polyline, d):
  if polyline.number_of_segments() < 1: return
  p = Polyline()
  for segment in polyline.get_segments():
    if segment.is_line():
      p.add_segment(parallel_line(segment, d))
      continue
    # Arc
    p.add_segment(parallel_arc(segment, -d))
  return p

def trim_parallels(parallels):
  '''
  Case 1: Line -> Line
  Case 2: Line -> Arc
  Case 3: Arc  -> Line
  Case 4: Arc  -> Arc

  For each of these cases we have two different possible outcomes
  Case 1: They intersect (Trim em)
  Case 2: They don't intersect (Connect via an arc)
  '''
  parallel_segments = parallels.get_segments()
  previous_segment  = parallel_segments[-1]
  points, bulges    = [], []
  for segment in parallel_segments:
    if previous_segment.is_line() and segment.is_line():
      point_of_intersection = _line_intersection_point(previous_segment, segment)
      if point_of_intersection is not None:
        points.append( point_of_intersection )
        bulges.append( 0 )
        previous_segment = segment
      else:
        arc_start_point, arc_end_point = previous_segment.end_point, segment.start_point
        bulge = 0.41421 # Calculate this
        bulge *= _determine_bulge_orientation(segment)
        points.extend( ( arc_start_point, arc_end_point ) )
        bulges.extend( ( bulge, 0 ) )
        previous_segment = segment
    elif previous_segment.is_line() and segment.is_arc():
      point_of_intersection = _line_and_arc_intersection_point(previous_segment, segment)
      if point_of_intersection is not None:
        points.append( point_of_intersection )
        bulges.append( 0 )
        previous_segment = segment
      else:
        previous_segment = segment
    elif previous_segment.is_arc() and segment.is_line():
      point_of_intersection = _line_and_arc_intersection_point(segment, previous_segment)
      if point_of_intersection is not None:
        points.append( point_of_intersection )
        bulges.append( previous_segment.bulge )
        previous_segment = segment
      else:
        previous_segment = segment
    else:
      # Two arcs
      point_of_intersection = _arc_intersection_point(previous_segment, segment)
      if point_of_intersection is not None:
        print('got here!')
        points.append( point_of_intersection )
        bulges.append( previous_segment.bulge )
        previous_segment = segment
      else:
        previous_segment = segment
  return _build_polyline_from_points_and_bulges( points, bulges )

def parallel_line(s, d):
  x1, y1      = s.start_point.x, s.start_point.y
  x2, y2      = s.end_point.x, s.end_point.y
  delta_x     = x2 - x1
  delta_y     = y2 - y1
  line_length = math.sqrt(delta_x**2 + delta_y**2)
  x_adj       = delta_y * (d/line_length)
  y_adj       = -delta_x * (d/line_length)
  return Segment( Point(x1 + x_adj, y1 + y_adj),
                  Point(x2 + x_adj, y2 + y_adj), 0 )

def parallel_arc(s, d):
  start_point, end_point = _determine_parallel_arc_start_and_end_points(s, d)
  return Segment( start_point, end_point, s.bulge )

def calculate_arc_center_point(s):
  if s.is_line(): return
  central_angle = s.central_angle()
  x1, y1        = s.start_point.x, s.start_point.y
  x2, y2        = s.end_point.x,   s.end_point.y
  m             = slope(s.start_point, s.end_point)
  new_slope     = -1/m if m != 0 else 0
  xm, ym        = (x1+x2)/2, (y1+y2)/2
  d_chord       = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
  d_perp        = d_chord / (2 * math.tan(central_angle/2))
  xc            = (d_perp) / math.sqrt(new_slope**2 + 1) + xm
  yc            = (new_slope)*(xc - xm) + ym
  return xc, yc

# Returns the slope between two points
def slope(p1, p2):
  if p2.x - p1.x != 0: return (p2.y - p1.y)/(p2.x - p1.x)
  return math.inf

def _determine_parallel_arc_start_and_end_points(s, d):
  x1, y1           = s.start_point.x, s.start_point.y
  x2, y2           = s.end_point.x,   s.end_point.y
  xc, yc           = calculate_arc_center_point(s)
  xm, ym           = (x1+x2)/2, (y1+y2)/2
  vec_x, vec_y     = xm - xc, ym - yc # vector points
  magnitude        = math.sqrt(vec_x**2 + vec_y**2)
  delta_x          = d * (vec_x/magnitude)
  delta_y          = d * (vec_y/magnitude)
  new_xc, new_yc   = xc + delta_x, yc + delta_y
  start_x, start_y = new_xc + (x1 - xc), new_yc + (y1 - yc)
  end_x, end_y     = new_xc + (x2- xc), new_yc + (y2 - yc)
  return Point(start_x, start_y), Point(end_x, end_y)

def _trim_line_and_arc(segment, next_segment):
  return

def _trim_arc_and_line(segment, next_segment):
  return

def _trim_two_arcs(segment, next_segment):
  return

# Code adapted from:
# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
def _line_intersection_point(segment, next_segment):
  def det(a, b, c, d): return a * d - b * c
  s_x1, s_y1   = segment.start_point.x,      segment.start_point.y
  s_x2, s_y2   = segment.end_point.x,        segment.end_point.y
  e_x1, e_y1   = next_segment.start_point.x, next_segment.start_point.y
  e_x2, e_y2   = next_segment.end_point.x,   next_segment.end_point.y
  start_x_diff = s_x1 - s_x2
  start_y_diff = s_y1 - s_y2
  end_x_diff   = e_x1 - e_x2
  end_y_diff   = e_y1 - e_y2
  div          = det(start_x_diff, end_x_diff, start_y_diff, end_y_diff)
  if div == 0: return None
  d1    = det(s_x1, s_y1, s_x2, s_y2)
  d2    = det(e_x1, e_y1, e_x2, e_y2)
  x     = det(d1, d2, start_x_diff, end_x_diff) / div
  y     = det(d1, d2, start_y_diff, end_y_diff) / div
  point = Point(x, y)
  # Add a check to see if the x and y coordinates are on the line segments, if not return False
  if _point_is_on_line_segment(point, next_segment): return point
  return None

def _line_and_arc_intersection_point(line_segment, arc_segment):
  from sympy.geometry import Circle, Point2D, Segment2D
  l_x1, l_y1 = line_segment.start_point.unpack()
  l_x2, l_y2 = line_segment.end_point.unpack()
  a_x1, a_y1 = arc_segment.start_point.unpack()
  a_x2, a_y2 = arc_segment.end_point.unpack()
  a_xc, a_yc = calculate_arc_center_point(arc_segment)
  radius     = abs( a_x1 - a_xc )
  A, B       = Point2D( l_x1, l_y1 ), Point2D( l_x2, l_y2 )
  AB_segment = Segment2D(A, B)
  c          = Circle( Point2D(a_xc, a_yc), radius )
  intersection_points = c.intersection(AB_segment)
  for point in intersection_points:
    x, y = point.x, point.y
    if min(a_x1,a_x2) <= x <= max(a_x1,a_x2) and min(a_y1,a_y2) <= y <= max(a_y1,a_y2):
      return Point(x, y)
  return None

def _arc_intersection_point(previous_segment, segment):
  from sympy.geometry import Circle, Point2D
  prev_x1          = previous_segment.start_point.x
  x1, y1           = segment.start_point.x, segment.start_point.y
  x2, y2           = segment.end_point.x, segment.end_point.y
  prev_xc, prev_yc = calculate_arc_center_point(previous_segment)
  xc, yc           = calculate_arc_center_point(segment)
  prev_radius      = abs( prev_x1 - prev_xc )
  radius           = abs( x1 - xc )
  print(prev_xc, prev_yc, prev_radius)
  print(xc, yc, radius)
  c1               = Circle( Point2D(prev_xc, prev_yc), prev_radius )
  c2               = Circle( Point2D(xc, yc), radius )
  intersection_points = c1.intersection(c2)
  if type(intersection_points) is not list: return None
  for point in intersection_points:
    x, y = float(point.x), float(point.y)
    print(min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2))
    print(min(x1,x2), '<=', x, '<=', max(x1,x2), min(y1,y2), '<=', y, '<=', max(y1,y2))
    if min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
      return Point(x, y)
  print()
  return None

def _build_polyline_from_points_and_bulges(points, bulges):
  if len(points) != len(bulges): return
  if len(points) == 0: return
  p = Polyline()
  for i in range(len(points) - 1):
    start_point, end_point, bulge = points[i], points[i+1], bulges[i]
    p.add_segment( Segment(start_point, end_point, bulge) )
  p.add_segment( Segment(points[-1], points[0], bulges[-1]) )
  return p

# This function operates under the assumption that the point given is at minimum on the extended
# line segment of segment. Only called by the _line_intersection_point function.
def _point_is_on_line_segment(point, segment):
  start_point, end_point = segment.start_point, segment.end_point
  x, y   = point.unpack()
  x1, y1 = start_point.unpack()
  x2, y2 = end_point.unpack()
  return min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2)

# returns 1 if bulge can stay the same, -1 if we should change orientation
def _determine_bulge_orientation(s):
  start_point, end_point = s.start_point, s.end_point
  x1, y1 = start_point.unpack()
  x2, y2 = end_point.unpack()
  # TODO: Write helper functions to make this read-able
  if x1 == x2 and y1 > y2:  return -1
  if x1 == x2 and y1 <= y2: return  1
  if y1 == y2 and x1 > x2:  return -1
  if y1 == y2 and x1 <= x2: return  1
  if y1 < y2  and x1 < x2:  return  1
  if y1 < y2  and x1 > x2:  return  1
  if y1 > y2  and x1 > x2:  return -1
  return -1

# # Efficient way to determine if two line segments intersect
# # Following 2 functions code taken from: 
# # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# def _ccw(A, B, C):
#     return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# # Return true if line segments AB and CD intersect
# def _line_segments_intersect(A, B, C, D):
#     return _ccw(A,C,D) != _ccw(B,C,D) and _ccw(A,B,C) != _ccw(A,B,D)
