from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from gpaw import GPAW, FermiDirac, PW

import argparse

parser = argparse.ArgumentParser()
defval = 2
parser.add_argument('-n', '--ID', type=int, default=defval,
                    help='ID of cluster 1 to 6 (default: {:.2f})'.format(defval))
defval = 4
parser.add_argument('-k', '--kpt', type=int, default=defval,
                    help='K value for kpts (default: {:.2f})'.format(defval))

args = parser.parse_args()

#connect to database and retrieve atoms object
db = connect("sub_100_Al-relaxed.db")
#sub_100_ids=[2, 3, 6, 7, 8, 10]

sub_100_ids = [args.ID]
k = args.kpt
calc = GPAW(mode=PW(300),
            xc='PBE',
            kpts=(k, k, k),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.01))


for cluster in db.select():
    atoms = cluster.toatoms()
    N_atoms = len(atoms)
    atoms.calc = calc

    atoms.get_potential_energy()
    Ef = calc.get_fermi_level()
    calc.fixed_density(
        nbands=16,
        symmetry='off',
        kpts={'path': 'GXWKL', 'npoints': 60},
        convergence={'bands': 8})
    Bs = calc.band_structure()
    bs.plot(filename='band_ID:'+str(args.ID)+'_k:'+str(k)+'.png', show=True, emax=10.0)
