from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM


#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
i=0
for cluster in db.select():
    atoms = cluster.toatoms()
    No_atoms = len(atoms)
    atoms.calc = calc
    pot_E = atoms.get_potential_energy()
    print(f'cohesive energy for index {i}: {pot_E/No_atoms} eV?')
    i += 1
