from ase import atoms
from ase.io import read, write
#from gpaw import GPAW
from ase.db import connect
from ase.calculators.eam import EAM


#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
for clusters in db:
    atoms = clusters.toatoms()
    atoms.calc = calc
    pot_E = atoms.get_potential_energy()
    print(pot_E)
