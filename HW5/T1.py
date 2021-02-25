from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS


#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')

f = open("clusters_pot.txt", "w")
f.write("cluster index, Natoms, total pot, pot/atom, \n")

i=0
for cluster in db.select():
    atoms = cluster.toatoms()
    N_atoms = len(atoms)
    atoms.calc = calc
    BFGS(atoms).run(fmax=0.01)
    pot_E = atoms.get_potential_energy()
    print(f'cohesive energy for index {i}: {pot_E/N_atoms} eV?')
    f.write(f"{i}, {N_atoms}, {pot_E}, {pot_E/N_atoms}\n")
    i += 1
