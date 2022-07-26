from structs.point import Point
from structs.segment import Segment
from structs.polyline import Polyline
from utils import get_parallels
from utils import trim_parallels
from plot import plot

# Global variable for boundary distance
DISTANCE = 1

# Main Method
def main():
  # Construct the original Polyline
  p = Polyline()

  # Straight positive slope polyline
  # p.add_segment( Segment(Point(0,0), Point(1,1), 0) )
  # p.add_segment( Segment(Point(1,1), Point(2,2), 0) )
  # p.add_segment( Segment(Point(2,2), Point(3,3), 0) )
  # p.add_segment( Segment(Point(3,3), Point(4,4), 0) )
  # p.add_segment( Segment(Point(4,4), Point(5,5), 0) )

  # Polyline with positive and negative slope portions
  # p.add_segment( Segment(Point(0,0), Point(1,1), 0) )
  # p.add_segment( Segment(Point(1,1), Point(2,2), 0) )
  # p.add_segment( Segment(Point(2,2), Point(3,2), 0) )
  # p.add_segment( Segment(Point(3,2), Point(4,1), 0) )
  # p.add_segment( Segment(Point(4,1), Point(5,0), 0) )

  # Hexagon Example
  # p.add_segment( Segment(Point(0,2), Point(1,3), 0) )
  # p.add_segment( Segment(Point(1,3), Point(2,3), 0) )
  # p.add_segment( Segment(Point(2,3), Point(3,2), 0) )
  # p.add_segment( Segment(Point(3,2), Point(2,1), 0) )
  # p.add_segment( Segment(Point(2,1), Point(1,1), 0) )
  # p.add_segment( Segment(Point(1,1), Point(0,2), 0) )

  # Arc Examples
  # p.add_segment( Segment(Point(1,1), Point(4,4), 0.41421) ) # 90deg central angle
  # p.add_segment( Segment(Point(1,4), Point(4,0), 0.41421) ) # 90deg central angle

  # Unit Circle Example
  # p.add_segment( Segment(Point(1,1),  Point(0,0),  0.41421) )
  # p.add_segment( Segment(Point(0,0),  Point(1,-1), 0.41421) )
  # p.add_segment( Segment(Point(1,-1), Point(2,0), -0.41421) ) # directionality is important for the bulge
  # p.add_segment( Segment(Point(2,0),  Point(1,1), -0.41421) ) # ditto

  # Bigger Circle Example
  p.add_segment( Segment(Point(0,3), Point(3,6),  0.41421) )
  p.add_segment( Segment(Point(3,6), Point(6,3), -0.41421) )
  p.add_segment( Segment(Point(6,3), Point(3,0), -0.41421) ) # directionality is important for the bulge
  p.add_segment( Segment(Point(3,0), Point(0,3), 0.41421) ) # ditto

  # Line and Arc Example
  # p.add_segment( Segment(Point(1,1), Point(3,3), 0) )
  # p.add_segment( Segment(Point(3,3), Point(5,5), 0.41421) )

  # Construct the parallel lines
  inner_parallels = get_parallels( p,  DISTANCE )
  # outer_parallels = get_parallels( p, -DISTANCE )

  # Trim the inner and outer parallels
  trimmed_inner_parallels = trim_parallels( inner_parallels )
  # trimmed_outer_parallels = trim_parallels(outer_parallels)

  # Plot results
  # plot( [ p ] )
  # plot( [ p, inner_parallels ] )
  # plot( [ p, outer_parallels ] )
  # plot( [ p, inner_parallels, outer_parallels ] )
  plot( [ p, trimmed_inner_parallels ] )
  # plot( [ p, trimmed_outer_parallels ] )
  # plot( [ p, trimmed_inner_parallels, trimmed_outer_parallels ] )
  # plot( [ p, inner_parallels, trimmed_inner_parallels ] )


# Script Entry Point
if __name__ == '__main__':
  main()