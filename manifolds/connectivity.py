import numpy as np
import matplotlib.pyplot as plt

def get_connectivity(distance_set, cutoff_radius, num_points, connected_sets=None):
  '''Get the connectivity between points. Two points are
     thought to be connected if the distance between them
     are smaller than cutoff_radius. Return a list of sets
     which are the sets each point belongs to.
     NOTE: the connected_sets argument will be MODIFIED!!!
  '''
  # If no pre-initialized connect_sets is given, set all points to be disconnected
 
  if connected_sets == None: 
    connected_sets = [ {i} for i in range(num_points) ]

  # Merge two sets if they are connected
  
  for distance in distance_set:
    i = distance[0]
    j = distance[1]
          
    if distance[2] < cutoff_radius:

      # Merge two sets

      if connected_sets[i] == connected_sets[j]:
        continue

      merged_set = connected_sets[i] | connected_sets[j]
      for k in merged_set:
        connected_sets[k] = merged_set

  return connected_sets


def wrap_connected_sets(connected_sets):
  '''Wrap the connected point sets into clusters'''
  cluster_list = []
   
  for s in connected_sets:
    if not s in cluster_list:
      cluster_list.append(s)

  return cluster_list


def get_attributes_vs_cutoffs(distance_matrix, cutoff_list, attribute_func):
  '''Get a list of attributes of connected_sets for a list of cutoffs.
     The calculation of attributes is defined by the attribute_func. 
  '''
  attribute_list = []
  connected_sets = None

  # Initialize the distance set
  
  distance_set = set()
  num_points = distance_matrix.shape[0]
  
  for i in range(num_points):
    for j in range(i+1, num_points):
      distance_set.add( (i, j, distance_matrix[i][j]) )
  
  # Calculate the attribute for each cutoff
  
  for cutoff in cutoff_list:
    connected_sets = get_connectivity(distance_set, cutoff, num_points, connected_sets)
    attribute_list.append(attribute_func(connected_sets))

    # Remove all the distances that is smaller than the cutoff
    # Because point pairs within those distances are already connected
    for distance in distance_set.copy():
      if distance[2] < cutoff:
        distance_set.remove(distance)

  return attribute_list


def plot_num_connected_manifolds_vs_cutoffs(distance_matrix, average_cutoff_list, dimension, save=None, title=''):
  '''Plot the number of connected manifolds against a list
     of average cutoffs.
  '''
  cutoff_list = [ np.sqrt(dimension) * c for c in average_cutoff_list ]

  def num_clusters(connected_sets):
    return len(wrap_connected_sets(connected_sets))

  num_connected_manifolds = get_attributes_vs_cutoffs(distance_matrix, cutoff_list, num_clusters)

  plt.clf()
  plt.plot(average_cutoff_list, num_connected_manifolds)
  plt.title(title)
  plt.xlabel('average cutoff')
  plt.ylabel('num clusters')
  
  if not save:
    plt.show()
  else:
    plt.savefig(save)


def plot_size_max_N_cluter(distance_matrix, average_cutoff_list, dimension, num_clusters=1, save=None, title=''):
  '''Plot the sizes of N max clusters for a list of average cutoffs.'''
  cutoff_list = [ np.sqrt(dimension) * c for c in average_cutoff_list ]

  def get_max_cluster_size(connected_sets):
    return sorted([len(connected_set) for connected_set in wrap_connected_sets(connected_sets)], reverse=True)
    
  max_sizes = get_attributes_vs_cutoffs(distance_matrix, cutoff_list, get_max_cluster_size)

  plt.clf()

  for i in range(num_clusters):
    max_i_sizes = [ s[i] if len(s) > i else 0 for s in max_sizes]
    plt.plot(average_cutoff_list, max_i_sizes)
  
  plt.title(title)
  plt.xlabel('average cutoff')
  plt.ylabel('max cluster size')
  
  if not save:
    plt.show()
  else:
    plt.savefig(save)

def plot_one_cluster_size(distance_matrix, average_cutoff_list, dimension, point_index, save=None, title=''):
  '''Plot the size of cluster that contains the given point.'''
  cutoff_list = [ np.sqrt(dimension) * c for c in average_cutoff_list ]

  class get_cluster_size:
    point = point_index
    def run(connected_sets):
      return len(connected_sets[get_cluster_size.point])
    
  sizes = get_attributes_vs_cutoffs(distance_matrix, cutoff_list, get_cluster_size.run)

  plt.clf()
  plt.plot(average_cutoff_list, sizes)
  plt.title(title)
  plt.xlabel('average cutoff')
  plt.ylabel('size of cluster contains point {0}'.format(point_index))
  
  if not save:
    plt.show()
  else:
    plt.savefig(save)

