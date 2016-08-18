#!/usr/bin/env python3

import os
import sys
import subprocess
import getpass
import pickle

from points_loaders.LoopLoader import LoopTorsionLoader
from metrics.distance_calculators import TorusDistance
from metrics.distance_matrix import calc_distance_matrix
from metrics.distance_matrix import plot_distance_distribution
from manifolds.connectivity import plot_num_connected_manifolds_vs_cutoffs
from manifolds.connectivity import plot_size_max_N_cluter 
from manifolds.connectivity import plot_one_cluster_size 
from manifolds.dimension import plot_local_dimension_of_points_on_torus

def analyze_one_protein(name):
  structure_dir = os.path.join(name, 'structures')
  pdb_list = [ os.path.join(structure_dir, f) for f in os.listdir(structure_dir) ]
   
  # Get loop terminals

  loop_terminals = LoopTorsionLoader.get_begin_end_from_loop_file(
                      os.path.join(name, name + '_native.pdb'),
                      os.path.join(name, name + '.loop'))
  dimension = (loop_terminals[1] - loop_terminals[0] + 1) * 2

  # Load points

  points = None

  if os.path.exists(os.path.join(name, 'cached_points.pickle')):
    with open(os.path.join(name, 'cached_points.pickle'), 'rb') as f:
      points = pickle.load(f)
     
  else:
    points = LoopTorsionLoader.load_from_pdbs(pdb_list, loop_terminals[0], loop_terminals[1])
    with open(os.path.join(name, 'cached_points.pickle'), 'wb') as f:
      pickle.dump(points, f, pickle.HIGHEST_PROTOCOL)

  # Get the distance matrix

  distance_matrix = None

  if os.path.exists(os.path.join(name, 'cached_distance_matrix.pickle')):
    with open(os.path.join(name, 'cached_distance_matrix.pickle'), 'rb') as f:
      distance_matrix = pickle.load(f)

  else:
    td_calc = TorusDistance(360)
    distance_matrix = calc_distance_matrix(points, td_calc)
    with open(os.path.join(name, 'cached_distance_matrix.pickle'), 'wb') as f:
      pickle.dump(distance_matrix, f, pickle.HIGHEST_PROTOCOL)

  # Save the figures
 
#  plot_distance_distribution(distance_matrix, 20,
#        180, dimension,
#        save=os.path.join(name, 'distance_distribution.png'),
#        title=name)

  plot_local_dimension_of_points_on_torus(points, 
        distance_matrix, 5, 360,
        save=os.path.join(name, 'local_dimensions.png'),
        title=name)
  
  average_cutoff_list = [ 180 * i / 300 for i in range(100) ]

#  plot_num_connected_manifolds_vs_cutoffs(distance_matrix,
#        average_cutoff_list,
#        dimension,
#        save=os.path.join(name, 'num_connected_manifolds_vs_cutoffs.png'),
#        title=name) 
  
#  plot_size_max_N_cluter(distance_matrix,
#        average_cutoff_list,
#        dimension,
#        num_clusters=5,
#        save=os.path.join(name, 'size_max_cluter.png'),
#        title=name) 

def get_content_of_one_protein(name):
  # Get figures

  analyze_one_protein(name)
  
  # Insert figures into the report

  figure_template = '''\
\\begin{{figure}}[h]
    \\centering
    \\caption{{{name}}}
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{distance_distribution_plot_path}}}}}
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{local_dimensions_plot_path}}}}}
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{num_cluster_plot_path}}}}}
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{size_max_cluster_plot_path}}}}}
\\end{{figure}}
'''
  
  return figure_template.format(
          name=name,
          distance_distribution_plot_path=os.path.join(name, 'distance_distribution.png'),
          local_dimensions_plot_path=os.path.join(name, 'local_dimensions.png'),
          num_cluster_plot_path=os.path.join(name, 'num_connected_manifolds_vs_cutoffs.png'),
          size_max_cluster_plot_path=os.path.join(name, 'size_max_cluter.png'))


def make_report(title):
  report_template = '''\
\\documentclass{{report}}
\\usepackage{{booktabs}}
\\usepackage{{graphicx}}
\\usepackage{{fullpage}}
\\usepackage{{hyperref}}
\\renewcommand{{\\textfraction}}{{0.00}}
\\hypersetup{{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}}
\\begin{{document}}
\\title{{{title}}}
\\author{{{author}}}
\\maketitle
\\tableofcontents
{chapters}
\\end{{document}}
'''
  
  # Get the content of the report
 
  content = ''
  
  for name in sorted(os.listdir('.')):

    if not os.path.isdir(name):
      continue
   
    content = content + get_content_of_one_protein(name) 

  # Write the .tex file

  with open('report.tex', 'w') as rf:
    rf.write(report_template.format(
              title=title,
              author=getpass.getuser(),
              chapters=content))
 
  # Generate report
  
  subprocess.call(['pdflatex', 'report.tex'])


if __name__ == '__main__':
  os.chdir(sys.argv[1])
  

  make_report('High-dim analysis report')
