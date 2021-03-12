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

parser = argparse.ArgumentParser()
defval = 3
parser.add_argument('-n', '--ID', type=int, default=defval,
                    help='ID of cluster 1 to 6 (default: {:.2f})'.format(defval))

args = parser.parse_args()

#if (args.redo_file):
#connect to database and retrieve atoms object
db = connect("sub_100_Al-relaxed.db")
#sub_100_ids=[2, 3, 6, 7, 8, 10]

#sub_100_ids = [args.ID]
#k = args.kpt
#else:
#    calc = GPAW('GPAW_ID_'+str(args.ID)+'_k:'+str(args.kpt)+'.gpw')
k = 8

for cluster in db.select(id=args.ID):
	atoms = cluster.toatoms()
	N_atoms = len(atoms)
	calc = GPAW(mode='fd',
            xc='PBE',
#            kpts=(k, k, k),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.01))
	atoms.calc = calc
	atoms.get_potential_energy()
	dos = DOS(calc, width = 0.2)
	d = dos.get_dos()
	e = dos.get_energies()
	fig = plt.figure()
	ax = fig.add_subplot()
	ax.plot(e,d)
	ax.set_xlabel('Energies [eV]')
	ax.set_ylabel('DOS')
	fig.savefig('DOS_'+str(N_atoms)+'.png')

"""
	print('potential:')
        atoms.get_potential_energy()
        print('fermi level')
        Ef = calc.get_fermi_level()
        calc.write('GPAW_ID_'+str(args.ID)+'_k:'+str(k)+'.gpw')
    calc = calc.fixed_density(
        nbands=16,
        symmetry='off',
        kpts={'path': 'GXULGK', 'npoints': 60},
        convergence={'bands': 8})
    print('band structure:')
    Bs = calc.band_structure()
    bs.plot(filename='band_ID:'+str(args.ID)+'_k:'+str(k)+'.png', show=True, emax=10.0)
"""
