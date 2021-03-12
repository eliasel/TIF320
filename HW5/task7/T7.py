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



atoms = bulk('Si', crystalstructure = 'diamond')
k = 50
calc = GPAW(mode=PW(300),
            xc='PBE',
            kpts=(k, k, k),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.01))

atoms.calc = calc
print('potential:')
atoms.get_potential_energy()
dos = DOS(calc, width = 0.2)
d = dos.get_dos()
e = dos.get_energies()

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

bs.plot(filename='Si_crystal_band.png', show=False, emax=10.0)

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(e,d)
ax.set_xlabel('Energy [ev]')
ax.set_ylabel('DOS')
fig.savefig('DOS_bulk.png')



