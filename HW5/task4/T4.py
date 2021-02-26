from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.phonons import Phonons
from ase.build import bulk
from ase.calculators.emt import EMT

import matplotlib.pyplot as plt

#connect to database and retrieve atoms object
atoms = bulk('Al', 'fcc', a=4.05)
calc = EAM(potential = 'al_potential.alloy')
#calc = EMT()
#atoms.calc = calc
ph = Phonons(atoms, calc, supercell = (7,7,7))
ph.run()
ph.read(acoustic = True)
ph.clean()

path = atoms.cell.bandpath('GXULGK', npoints = 100)
bs = ph.get_band_structure(path)
fig = plt.figure(1, figsize=(7,4))
ax = fig.add_axes([.12, .07, .67, .85])
bs.plot(ax=ax)

fig.savefig('Al-bulk.png')
