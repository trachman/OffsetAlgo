class Polyline:

  def __init__(self):
    self.segments = []

  def __str__(self):
    return '\n'.join( [ str(segment) for segment in self.segments ] )

  def __getitem__(self, index):
    if not (0 <= index < len(self.segments)): return
    return self.segments[index]

  def add_segment(self, segment):
    self.segments.append(segment)

  def add_segments(self, segments):
    self.segments.extend(segments)

  def get_segments(self):
    return self.segments

  def number_of_segments(self):
    return len(self.segments)
