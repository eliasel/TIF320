from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.build import bulk
import numpy as np

atoms = bulk('Al')
calc = EAM(potential = 'al_potential.alloy')
atoms.calc = calc
#pot_E = atoms.get_potential_energy()
#print(f'cohesive energy for bulk Al: {pot_E} eV?')
#print(atoms.cell)
start_cell = atoms.cell
a = np.linspace(1.5,2.5,4000)
energies = np.zeros(4000)
i=0
for a in a:
    atoms.set_cell(start_cell/2.025*a)
    energies[i] = atoms.get_potential_energy()
    print(f'{start_cell/2.025*a} energy :  {energies[i]}')
    i += 1
