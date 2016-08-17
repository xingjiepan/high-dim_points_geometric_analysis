import numpy as np
import matplotlib.pyplot as plt


def calc_distance_matrix(point_list, distance_calculator):
  '''Calculate the distance between each pair of points in point_list.'''
  num_points = len(point_list)
  distance_matrix = np.zeros((num_points, num_points))
  
  for i in range(num_points):
    for j in range(i+1, num_points):
      distance_matrix[i][j] = distance_calculator.calc(point_list[i], point_list[j])
      distance_matrix[j][i] = distance_matrix[i][j]
  
  return distance_matrix  


def plot_distance_distribution(distance_matrix,
    num_bins, average_cutoff, dimension, save=None, title=''):
  '''Plot the distance distribution.'''
  num_points = distance_matrix.shape[0]
  
  # Initialize the distance list
  
  distance_list = []
  
  for i in range(num_points):
    for j in range(i+1, num_points):
      distance_list.append(distance_matrix[i][j])
      
  distance_list_sorted = sorted(distance_list)
  
  # Sort distance into bins
  
  bin_size = average_cutoff / num_bins 
  bins = [ i * bin_size for i in range(num_bins) ]
  bin_volume = [ 0 for i in range(num_bins) ]

  dim_factor = np.sqrt(dimension)

  j = 0
  for i in range(num_bins):
    
    while j < len(distance_list_sorted) \
          and distance_list_sorted[j] < dim_factor * (bins[i] + bin_size):
      bin_volume[i] += 1
      j += 1

  while j < len(distance_list_sorted):
    bin_volume[-1] += 1
    j += 1

  # Make a bar plot

  plt.clf()
  plt.bar(bins, bin_volume, width=bin_size)
  plt.title(title)
  plt.xlabel('distance')
  plt.ylabel('number of distances')

  if not save:
    plt.show()
  else:
    plt.savefig(save)
