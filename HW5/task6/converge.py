from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from gpaw import GPAW, FermiDirac, PW
from ase.build import bulk 
from ase.dft import *
import matplotlib.pyplot as plt

import argparse



atoms = bulk('Al')

k = 8
calc = GPAW(mode=PW(300),
            xc='PBE',
            kpts=(k, k, k),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.01))

atoms.calc = calc
e = atoms.get_potential_energy()

print('hej: ' + str(e))


"""
fig = plt.figure()
ax = fig.add_subplot()
ax.plot(e,d)
ax.set_xlabel('Energy [ev]')
ax.set_ylabel('DOS')
fig.savefig('DOS_bulk.png')
"""


