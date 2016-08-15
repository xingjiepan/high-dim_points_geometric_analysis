'''Calculate different types of distances between points.'''

import numpy as np


class TorusDistance:
  '''Calculate the distance between two points on a torus.'''
  def __init__(self, torus_length):
    self.torus_length = torus_length
  
  def calc(self, p1, p2):
    if p1.shape != p2.shape:
      raise Exception('The dimension of {0} is not equal to {1}'.format(p1, p2))

    mod_diff1 = (p1 - p2) % self.torus_length 
    mod_diff2 = (p2 - p1) % self.torus_length 
    min_diff = np.minimum(mod_diff1, mod_diff2)

    return np.sqrt(np.sum(min_diff**2))

