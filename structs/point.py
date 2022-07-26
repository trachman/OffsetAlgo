class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, obj) -> bool:
    return self.x == obj.x and self.y == obj.y

  def __str__(self):
    return f'({self.x},{self.y})'

  def unpack(self):
    return self.x, self.y
