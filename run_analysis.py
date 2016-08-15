#!/usr/bin/env python3

import os

from points_loaders.LoopLoader import LoopTorsionLoader
from metrics.distance_calculators import TorusDistance
from metrics.distance_matrix import calc_distance_matrix

pdb_dir = 'inputs/test/30_KIC_with_fragments_1arb_RolandFragsInputsSettings_ideal'
pdb_list = [ os.path.join(pdb_dir, f) for f in os.listdir(pdb_dir) ]

points = LoopTorsionLoader.load_from_pdbs(pdb_list[0:20], 182, 193)
#print(points)

td_calc = TorusDistance(360)
distance_matrix = calc_distance_matrix(points, td_calc)
print(distance_matrix) 
