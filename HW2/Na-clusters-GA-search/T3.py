import numpy as np
from ase import Atoms
from ase.db import connect
from ase.ga.data
from ase.optimize import GPMin


from gpaw import GPAW

#connection to database
db = connect("atomisar.db")
number_of_atom_clusters = db.count('natoms>0') 

calc = GPAW(nbands=10, txt='out.txt', mode='lcao', basis='dzp')

for atom_cluster in db:
  atoms = atom_cluster.toatoms()
  atoms.calc = calc  
  #print(atoms) 
  dynamics = GPMin(atoms)
  dynamics.run(fmax=0.02, steps=100)
  