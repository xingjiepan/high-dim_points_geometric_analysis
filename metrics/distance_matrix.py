import numpy as np


def calc_distance_matrix(point_list, distance_calculator):
  '''Calculate the distance between each pair of points in point_list.'''
  num_points = len(point_list)
  distance_matrix = np.zeros((num_points, num_points))
  
  for i in range(num_points):
    for j in range(i+1, num_points):
      distance_matrix[i][j] = distance_calculator.calc(point_list[i], point_list[j])
      distance_matrix[j][i] = distance_matrix[i][j]
  
  return distance_matrix  
  
