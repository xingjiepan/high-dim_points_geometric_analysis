#!/usr/bin/env python3

import os
import pickle

from points_loaders.LoopLoader import LoopTorsionLoader
from metrics.distance_calculators import TorusDistance
from metrics.distance_matrix import calc_distance_matrix
from manifolds.connectivity import plot_num_connected_manifolds_vs_cutoffs
from manifolds.connectivity import plot_size_max_cluter 
from manifolds.connectivity import plot_one_cluster_size 


#pdb_dir = 'inputs/test/30_KIC_with_fragments_1arb_RolandFragsInputsSettings_ideal'
#pdb_list = [ os.path.join(pdb_dir, f) for f in os.listdir(pdb_dir) ]
#
#points = LoopTorsionLoader.load_from_pdbs(pdb_list, 182, 193)
##print(points)

td_calc = TorusDistance(360)
#max_distance = td_calc.max_distance(points[0].shape[0])
##print(max_distance)

#distance_matrix = calc_distance_matrix(points, td_calc)
##print(distance_matrix)

#with open('test_dist_matrix.pickle', 'wb') as f:
#  pickle.dump( distance_matrix, f, pickle.HIGHEST_PROTOCOL )

distance_matrix = None
with open('test_dist_matrix.pickle', 'rb') as f:
  distance_matrix = pickle.load(f)

average_cutoff_list = [ 180 * i / 300 for i in range(100) ]
#plot_num_connected_manifolds_vs_cutoffs(distance_matrix, average_cutoff_list, 24) 
plot_size_max_cluter(distance_matrix, average_cutoff_list, 24) 
#plot_one_cluster_size(distance_matrix, average_cutoff_list, 24, 0) 
