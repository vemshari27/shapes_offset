# Generic imports
import os
import sys
import pygmsh, meshio
from shapely.geometry import Polygon

# Custom imports
from shapes import *

offset_dist = 0.5
num_sample_points = 50
save_file = "sample_points.csv"

### ************************************************
### Generate a shape from in-house csv format
# Check number of input arguments
if (len(sys.argv) != 2):
    print('Incorrect number of input arguments')
    print('Correct usage :')
    print(' python3 generate_shape_from_file.py filename')
    sys.exit(0)

# Retrieve input arguments
filename = sys.argv[1]
if (not os.path.isfile(filename)):
    print('Input file does not exist')
    quit()

# Generate shape
shape = Shape()
shape.read_csv(filename)
shape.generate(ccws=True,
               centering=True, magnify=5)


points = shape.curve_pts[:,:-1]
# polygon = Polygon(points)
# offset_polygon = polygon.buffer(offset_dist, )

# x, y = offset_polygon.exterior.xy
# for i in range(len(x))
points = points.tolist()
sample_points = points[::int(len(points)/num_sample_points)]
with open(save_file, 'w') as f:
    for p in sample_points:
        f.write('{},{}\n'.format(*p))