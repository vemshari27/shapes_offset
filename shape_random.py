# Custom imports
import os
import sys
import pygmsh, meshio
import csv
from shapely.geometry import Polygon

from shapes import *

### ************************************************
### Generate a random shape from given inputs
filename       = 'shape'
n_pts          = 4
n_sampling_pts = 50
plot_pts       = True
mesh_domain    = False
magnify        = 5.0
domain_h       = 0.2
xmin           =-2.0
xmax           = 5.0
ymin           =-2.0
ymax           = 2.0
offset_dist = 1
waypoints_file = '/home/fleeting/ISU/sem1/COMS_5760/project/UAVSurveillance/src/ground_control/config/path_polygon.csv'
waypoints_file_1 = '/home/fleeting/ISU/sem1/COMS_5760/project/UAVSurveillance/src/ground_control/config/shape_polygon.csv'

# To generate shapes with homogeneous curvatures
radius         = [0.5]
edgy           = [0.0]

# To generate shapes with random curvatures
#radius         = np.random.uniform(low=0.0, high=1.0, size=n_pts)
#edgy           = np.random.uniform(low=0.0, high=1.0, size=n_pts)

# Generate and mesh shape
shape = Shape(filename,
              None,
              n_pts,
              n_sampling_pts,
              radius,
              edgy)
shape.generate(magnify = magnify)
# shape.mesh(    mesh_domain = mesh_domain,
#                domain_h    = domain_h,
#                xmin        = xmin,
#                xmax        = xmax,
#                ymin        = ymin,
#                ymax        = ymax)
shape.generate_image(plot_pts = plot_pts,
                     xmin     = xmin,
                     xmax     = xmax,
                     ymin     = ymin,
                     ymax     = ymax,
                     show_quadrants = True)
shape.write_csv()

points = shape.curve_pts[:,:-1]
polygon = Polygon(points)
offset_polygon = polygon.buffer(offset_dist, )

x, y = polygon.exterior.xy
points = list(zip(x, y))
print(len(points))
with open(waypoints_file_1, 'w') as f:
    for x,y in points:
        f.write(f"{x},{y}\n")

x, y = offset_polygon.exterior.xy
points = list(zip(x, y))
points = points[::int(len(points)/50)]

with open(waypoints_file, 'w') as f:
    for x,y in points:
        f.write(f"{x},{y}\n")

points_2d = np.array(points)
# Define the height of the extrusion
height = 5.0  # Change this to your desired height

# Create vertices for the bottom and top faces
bottom_vertices = np.c_[points_2d, np.zeros(len(points_2d))]  # z=0 for bottom face
top_vertices = np.c_[points_2d, np.full(len(points_2d), height)]  # z=height for top face

# Combine both to form the 3D vertices array
vertices = np.vstack([bottom_vertices, top_vertices])

num_points = len(points_2d)
faces = []

# Bottom face triangles (assumes the points are ordered)
for i in range(1, num_points - 1):
    faces.append([0, i, i + 1])

# Top face triangles
offset = num_points
for i in range(1, num_points - 1):
    faces.append([offset, offset + i + 1, offset + i])

# Side faces (each side between a pair of vertices)
for i in range(num_points):
    next_i = (i + 1) % num_points
    faces.append([i, next_i, next_i + offset])
    faces.append([i, next_i + offset, i + offset])

# Convert faces into numpy array
faces = np.array(faces)

# Create the mesh object
mesh = meshio.Mesh(points=vertices, cells={"triangle": faces})

# Save as COLLADA .dae file
mesh.write("mesh_target.stl", file_format="stl")
