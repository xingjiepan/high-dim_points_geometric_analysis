#!/usr/bin/env python3

import os
import pickle

from points_loaders.LoopLoader import LoopTorsionLoader
from metrics.distance_calculators import TorusDistance
from metrics.distance_matrix import calc_distance_matrix
from manifolds.dimension import plot_local_dimension_of_points_on_torus


#pdb_dir = 'tests/30_KIC_with_fragments_1arb_RolandFragsInputsSettings_ideal'
#pdb_list = [ os.path.join(pdb_dir, f) for f in os.listdir(pdb_dir) ]
#
#points = LoopTorsionLoader.load_from_pdbs(pdb_list, 182, 193)
##print(points)

#td_calc = TorusDistance(360)
#max_distance = td_calc.max_distance(points[0].shape[0])
##print(max_distance)

#distance_matrix = calc_distance_matrix(points, td_calc)
##print(distance_matrix)

#with open('test_points.pickle', 'wb') as f:
#  pickle.dump(points, f, pickle.HIGHEST_PROTOCOL)

#with open('test_dist_matrix.pickle', 'wb') as f:
#  pickle.dump( distance_matrix, f, pickle.HIGHEST_PROTOCOL )

points = None
with open('test_points.pickle', 'rb') as f:
  points = pickle.load(f)

distance_matrix = None
with open('test_dist_matrix.pickle', 'rb') as f:
  distance_matrix = pickle.load(f)

plot_local_dimension_of_points_on_torus(points, distance_matrix, 5, 360)
