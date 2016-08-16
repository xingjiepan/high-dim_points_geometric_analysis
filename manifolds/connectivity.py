import matplotlib.pyplot as plt

def get_connectivity(distance_matrix, cutoff_radius):
  '''Get the connectivity between points. Two points are
     thought to be connected if the distance between them
     are smaller than cutoff_radius. Return a list of sets
     where each set contains some connected points.
  '''
  num_points = distance_matrix.shape[0]
  
  # Set all points to be disconnected
  
  connected_sets = [ {i} for i in range(num_points) ]

  # Merge two sets if they are connected
  
  for i in range(num_points):
    for j in range(i+1, num_points):
      
      if distance_matrix[i][j] < cutoff_radius:

        # Merge two sets

        if connected_sets[i] == connected_sets[j]:
          continue

        merged_set = connected_sets[i] | connected_sets[j]
        for k in merged_set:
          connected_sets[k] = merged_set

  # Wrap the connected point sets into a list
   
  return_list = []
   
  for s in connected_sets:
    if not s in return_list:
      return_list.append(s)

  return return_list


def get_num_connected_manifolds(distance_matrix, cutoff_list):
  '''Get the number of connected manifolds for a list of cutoffs.'''
  return [ len(get_connectivity(distance_matrix, cutoff)) for cutoff in cutoff_list ]


def plot_num_connected_manifolds_vs_cutoffs(distance_matrix, cutoff_list):
  '''Plot the number of connected manifolds against a list
     of cutoffs.
  '''
  num_connected_manifolds = get_num_connected_manifolds(distance_matrix, cutoff_list)

  plt.plot(cutoff_list, num_connected_manifolds)
  plt.show()


def get_size_max_cluster(distance_matrix, cutoff_list):
  '''Get the max size of clusters for a list of cutoffs.'''
  max_sizes = []
  for cutoff in cutoff_list:
    sizes = [ len(connected_sets) for connected_sets in get_connectivity(distance_matrix, cutoff) ]
    max_sizes.append(max(sizes))
  return max_sizes


def plot_size_max_cluter(distance_matrix, cutoff_list):
  '''Plot the max size of clusters for a list of cutoffs.'''
  max_sizes = get_size_max_cluster(distance_matrix, cutoff_list)

  plt.plot(cutoff_list, max_sizes)
  plt.show()
