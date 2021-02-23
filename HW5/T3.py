from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.vibrations import Vibrations
#from ase.optimize import BFGS #They use this in example


#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
i=0
for cluster in db.select():
    atoms = cluster.toatoms()
    No_atoms = len(atoms)
    atoms.calc = calc
    pot_E = atoms.get_potential_energy()
    
    i += 1
