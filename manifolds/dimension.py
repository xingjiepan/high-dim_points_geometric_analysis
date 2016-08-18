import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def torus_points_normalizer(points, torus_length):
  '''Nomarlize a set of points on a torus by moving
     the points to the center of the cutted torus.
     The span of the point set shouldn't be too big. 
  '''
  dim = points[0].shape[0]

  shift = torus_length / 2 * np.ones(dim) - points[0]

  return [ (p + shift) % torus_length for p in points ]


def get_dimension_of_points(points):
  '''Get the dimension of a list of points.
     A dimension is negligible if its eigenvalue is 
     smaller than the 1/5 of the highest eigen value.
  '''
  if len(points) < 2:
    return 0

  embeded_dim = points[0].shape[0]
  
  pca = PCA(n_components=embeded_dim)
  pca.fit(points)

  ev_max = pca.explained_variance_ratio_[0]
  significant_evs = [ ev for ev in pca.explained_variance_ratio_ if ev > 0.1 * ev_max ]

  return len(significant_evs)


def plot_local_dimension_of_points_on_torus(points, distance_matrix, average_cutoff, torus_length, save=None, title=''):
  '''Plot the local dimensions of points on a torus.'''
  cutoff = np.sqrt(points[0].shape[0]) * average_cutoff
  indices = set([ i for i in range(len(points)) ])
  
  # Group points into local clusters and calculate the dimensions

  cluster_sizes = []
  dimensions = []

  while 0 != len(indices):
    i = indices.pop()
    indices.add(i)
    local_cluster = []
    
    for j in range(len(points)):
      
      if distance_matrix[i][j] < cutoff:
        local_cluster.append(points[j])
        
        if j in indices:
          indices.remove(j)

    cluster_sizes.append(len(local_cluster))
    
    normalized_points = torus_points_normalizer(local_cluster, torus_length)
    dimensions.append(get_dimension_of_points(normalized_points))

  # Draw the plot

  plt.clf()
  plt.scatter(cluster_sizes, dimensions, alpha=0.3)
  plt.title(title)
  plt.xlabel('local cluster size')
  plt.ylabel('dimension')
  
  if not save:
    plt.show()
  else:
    plt.savefig(save)
