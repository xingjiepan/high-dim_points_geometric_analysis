import numpy as np
import Bio.PDB as PDB

from .sidechain_definition_table import sidechain_definition_table

class LoopTorsionLoader:
  '''Load the torsions of loops into points.'''
  def __init__(self):
    pass

  def load_from_pdbs(pdb_list, begin_num, end_num, model=0, chain='A'):
    point_list = []

    for fpdb in pdb_list:
      loop = Loop(begin_num, end_num, fpdb, model, chain)
      
      # Load the torsions of a loop into a numpy array

      new_point = []
      for i in range(len(loop.torsions['phi'])):
        new_point.append(loop.torsions['phi'][i])
        new_point.append(loop.torsions['psi'][i])

      point_list.append(np.array(new_point))

    return point_list

  def get_begin_end_from_loop_file(pdb_file, loop_file, model=0, chain='A'):
    '''Get the begin and end of a loop from a loop file.
       Note that the numbers in a loop file are rosetta numbers,
       while the begin and end are PDB file numbers.
    '''
    # Read Rosetta loop terminals
    
    rosetta_begin = 0
    rosetta_end = 0

    with open(loop_file, 'r') as lf:
      line = lf.readline()
      rosetta_begin = int(line.split()[1])
      rosetta_end = int(line.split()[2])

    # Convert Rosetta numbers into pdb numbers

    parser = PDB.PDBParser()
    structure = parser.get_structure('', pdb_file)

    residue_list = [ r for r in structure[model][chain] ]

    return (residue_list[rosetta_begin].get_id()[1], residue_list[rosetta_end].get_id()[1])


class Loop:
  '''A simple helper class which defines the torsions of a loop.'''
  def __init__(self, begin_num, end_num, pdb_file_name, model=0, chain='A'):
    parser = PDB.PDBParser()
    structure = parser.get_structure('', pdb_file_name)

    self.torsions = {'phi':[], 'psi':[]}
    for i in range(begin_num, end_num+1):
      self._add_residue( structure[model][chain][i], structure[model][chain][i-1] )

  def _add_residue(self, residue, prev_residue):
    self.torsions['phi'].append( self._calc_phi(residue, prev_residue) )
    self.torsions['psi'].append( self._calc_psi(residue) )

  def _calc_phi(self, residue, prev_residue):
    vH = residue['CD'].get_vector() if residue.get_resname()=='PRO' \
                                    else prev_residue['C'].get_vector()
    vN = residue['N'].get_vector()
    vCA = residue['CA'].get_vector()
    vR = residue[ sidechain_definition_table[residue.get_resname()] ].get_vector()
    return np.rad2deg( PDB.calc_dihedral(vH, vN, vCA, vR) )

  def _calc_psi(self, residue):
    vR = residue[ sidechain_definition_table[residue.get_resname()] ].get_vector()
    vCA = residue['CA'].get_vector()
    vC = residue['C'].get_vector()
    vO = residue['O'].get_vector()
    return np.rad2deg( PDB.calc_dihedral(vR, vCA, vC, vO) )


