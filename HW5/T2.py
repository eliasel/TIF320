from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.build import bulk
import numpy as np
from ase.optimize import BFGS


atoms = bulk('Al')
calc = EAM(potential = 'al_potential.alloy')
atoms.calc = calc

f = open("energy_v_lattice.txt", "w")
f.write("lattice, energy\n")

start_cell = atoms.cell/2.025
a = np.linspace(1.7,2.5,3000)
energies = np.zeros(4000)
i=0
min_energy = 10
best_a = 0
for a in a:
    atoms.set_cell(start_cell*a)
    BFGS(atoms).run(fmax=0.01)
    energies[i] = atoms.get_potential_energy()
    #Use BFGS to minimize the structure?

    f.write(f"{start_cell/2.025*a}, {energies[i]}\n")
    i += 1
    if (energies[i]>min_energy):
        best_a = a


write('bulk_Al.db', atoms.set_cell(start_cell*best_a))
