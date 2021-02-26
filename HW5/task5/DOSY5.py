from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from gpaw import GPAW, FermiDirac, PW
from ase.build import bulk
from ase.dft import *

import argparse

parser = argparse.ArgumentParser()
defval = 4
parser.add_argument('-k', '--kpt', type=int, default=defval,
                    help='K value for kpts (default: {:.2f})'.format(defval))

args = parser.parse_args()

atoms = bulk('Al')

k = args.kpt
calc = GPAW(mode=PW(300),
            xc='PBE',
            kpts=(k, k, k),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.01))

atoms.calc = calc
print('potential:')
atoms.get_potential_energy()
print('fermi level')
Ef = calc.get_fermi_level()
calc.write('bulk.gpw')
calc = calc.fixed_density(
        nbands=16,
        symmetry='off',
        kpts={'path': 'GXULGK', 'npoints': 60},
        convergence={'bands': 8})
print('band structure:')
bs = calc.band_structure()

#bs.plot(filename='k:'+str(k)+'bulk.png', show=False, emax=10.0)

dos = ph.get_dos(kpts=(8, 8, 8)).sample_grid(npts=60, width=None)

# Plot the band structure and DOS:
import matplotlib.pyplot as plt  # noqa
fig = plt.figure(1, figsize=(7, 4))
ax = fig.add_axes([.12, .07, .67, .85])

emax = 0.035
bs.plot(ax=ax, emin=0.0, emax=emax)

dosax = fig.add_axes([.8, .07, .17, .85])
dosax.fill_between(dos.weights[0], dos.energy, y2=0, color='grey',
                   edgecolor='k', lw=1)

dosax.set_ylim(0, emax)
dosax.set_yticks([])
dosax.set_xticks([])
dosax.set_xlabel("DOS", fontsize=18)

fig.savefig('Al_phonon.png')
