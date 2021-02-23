from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.build import bulk
import numpy as np

atoms = bulk('Al')
calc = EAM(potential = 'al_potential.alloy')
atoms.calc = calc

f = open("energy_v_lattice.txt", "w")
f.write("lattice, energy\n")

start_cell = atoms.cell/2.025
a = np.linspace(1.5,2.5,4000)
energies = np.zeros(4000)
i=0
for a in a:
    atoms.set_cell(start_cell*a)
    energies[i] = atoms.get_potential_energy()
    #print(f'{start_cell/2.025*a} energy :  {energies[i]}')
    f.write(f"{start_cell/2.025*a}, {energies[i]}\n")
    i += 1
