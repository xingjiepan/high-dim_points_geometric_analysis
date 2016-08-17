#!/usr/bin/env python3

import os
import sys
import subprocess
import getpass

from points_loaders.LoopLoader import LoopTorsionLoader
from metrics.distance_calculators import TorusDistance
from metrics.distance_matrix import calc_distance_matrix
from metrics.distance_matrix import plot_distance_distribution
from manifolds.connectivity import plot_num_connected_manifolds_vs_cutoffs
from manifolds.connectivity import plot_size_max_N_cluter 
from manifolds.connectivity import plot_one_cluster_size 


def analyze_one_protein(name):
  structure_dir = os.path.join(name, 'structures')
  pdb_list = [ os.path.join(structure_dir, f) for f in os.listdir(structure_dir) ]
   
  # Get loop terminals

  loop_terminals = LoopTorsionLoader.get_begin_end_from_loop_file(
                      os.path.join(name, name + '_native.pdb'),
                      os.path.join(name, name + '.loop'))
  dimension = (loop_terminals[1] - loop_terminals[0] + 1) * 2

  # Load points

  points = LoopTorsionLoader.load_from_pdbs(pdb_list, loop_terminals[0], loop_terminals[1])


  # Get the distance matrix

  td_calc = TorusDistance(360)
  distance_matrix = calc_distance_matrix(points, td_calc)

  # Save the figures
 
  plot_distance_distribution(distance_matrix, 20,
        180, dimension,
        save=os.path.join(name, 'distance_distribution.png'),
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

  #analyze_one_protein(name)
  
  # Insert figures into the report

  figure_template = '''\
\\begin{{figure}}[h]
    \\centering
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{distance_distribution_plot_path}}}}}
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{num_cluster_plot_path}}}}}
    \\parbox{{3in}}{{\\includegraphics[width=3in]{{{size_max_cluster_plot_path}}}}}
\\end{{figure}}
'''
  
  return figure_template.format(
          distance_distribution_plot_path=os.path.join(name, 'distance_distribution.png'),
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
