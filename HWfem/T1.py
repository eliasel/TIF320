from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM


#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
i=0
for clusters in db.select():
    atoms = clusters.toatoms()
    atoms.calc = calc
    pot_E = atoms.get_potential_energy()
    print(f'cohesive energy for index {i}: {pot_E} eV?')
    i += 1
