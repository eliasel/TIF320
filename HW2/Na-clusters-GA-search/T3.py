import numpy as np
from ase import Atoms
from ase.db import connect
from ase.optimize import GPMin
from ase.io import write

from gpaw import GPAW, FermiDirac

#connection to database
db = connect("atomisar.db")
#number_of_atom_clusters = db.count('natoms>0') 

calc = GPAW(nbands=10,
	    h=0.25,
	    txt ='out.txt',
	    occupations=FermiDirac(0.05),
	    setups={'Na': '1'},
	    mode='lcao',
	    basis = 'dzp')

for atom_cluster_rows in db.select():
  atoms = atom_cluster_rows.toatoms()
  atoms.calc = calc  
  #print(atoms) 
  dynamics = GPMin(atoms, trajectory = 'relax.traj', logfile ='log.log' )
  dynamics.run(fmax=0.02, steps=100)
  energy = atoms.get_total_energy()
  
  write('ground_states.xyz', atoms)

