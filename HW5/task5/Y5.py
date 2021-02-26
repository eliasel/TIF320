from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from gpaw import GPAW, FermiDirac, PW

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
Bs = calc.band_structure()

bs.plot(filename='bulk.png', show=True, emax=10.0)
