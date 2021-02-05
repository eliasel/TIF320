import numpy as np
from ase import Atoms
from ase.db import connect
from ase.optimize import GPMin
from ase.io import write 

from gpaw import GPAW, FermiDirac
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mode', help = 'set the mode for GPAW allowed modes fd, lcao or pw') 

defval = 10
parser.add_argument('-n', '--nbands', type=int, default=defval, help='nbands value for GPAW (default: {})'.format(defval))

defval = 0.25
parser.add_argument( '--hval', type=float, default=defval, help='Value of h in GPAW (default: {})'.format(defval))

args = parser.parse_args()



#connection to database
db = connect("atomisar.db")
number_of_atom_clusters = db.count('natoms>0') 

#print(f'running in {args.mode} mode')
#set calculator parameters
if (args.mode == 'lcao'):

  calc = GPAW(nbands=args.nbands,
            h=args.hval,
            txt='out.txt',
            occupations=FermiDirac(0.05),
            setups={'Na': '1'},
            mode=args.mode,
            basis='dzp')
if (args.mode ==  'fd'):
  calc = GPAW(nbands=args.nbands,
            h=args.hval,
            txt='out.txt',
            occupations=FermiDirac(0.05),
            setups={'Na': '1'},
            mode=args.mode)
if (args.mode ==  'pw'):
  calc = GPAW(nbands=args.nbands,
            h=args.hval,
            txt='out.txt',
            occupations=FermiDirac(0.05),
            setups={'Na': '1'},
            mode=args.mode)


#Loop over all clusters and relax them
for atom_cluster in db.select():
  atoms = atom_cluster.toatoms()
  atoms.calc = calc  
  #print(atoms) 
  dynamics = GPMin(atoms)
  dynamics.run(fmax=0.02, steps=100)
  
  #Write minimized cluster to xyz datafile 
  write(f'gs_{args.mode}_n{nbands}_.xyz', atoms)
