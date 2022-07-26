import math

class Segment:

  def __init__(self, start_point, end_point, bulge):
    self.start_point = start_point
    self.end_point = end_point
    self.bulge = bulge

  def __eq__(self, obj):
    return self.start_point == obj.start_point and self.end_point == obj.end_point and self.bulge == obj.bulge

  def __str__(self):
    return f'[{str(self.start_point), str(self.end_point), {self.bulge}}]'

  def is_line(self):
    return self.bulge == 0

  def is_arc(self):
    return self.bulge != 0

  def central_angle(self):
    if self.bulge == 0: return
    return 4 * math.atan(self.bulge)
