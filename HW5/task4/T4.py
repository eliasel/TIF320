from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.phonons import Phonons
from ase.build import bulk

import matplotlib.pyplot as plt

#connect to database and retrieve atoms object
atoms = bulk('Al')
#calc = EAM(potential = 'al_potential.alloy')
calc = EAM()
atoms.calc = calc
ph = Phonons(atoms, calc, supercell = (7,7,7))
ph.run()
ph.read(acoustic = True)

path = atoms.cell.bandpath('GXULGK', npoints = 100)
bs = ph.get_band_structure(path)
fig = plt.figure(1, figsize=(7,4))
ax = fig.add_axes([.12, .07, .67, .85])
bs.plot(ax=ax)

fig.savefig('Al-bulk.png')
