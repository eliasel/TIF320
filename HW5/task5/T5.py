from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from gpaw import GPAW, FermiDirac, PW

import argparse
"""
parser = argparse.ArgumentParser()
defval = 2
parser.add_argument('-n', '--ID', type=int, default=defval,
                    help='ID of cluster 1 to 6 (default: {:.2f})'.format(defval))
defval = 4
parser.add_argument('-k', '--kpt', type=int, default=defval,
                    help='K value for kpts (default: {:.2f})'.format(defval))

default = True
parser.add_argument('-f', '--redo_file', type=bool, default=default,
                    help='redo calculations for get potential? (default: {:.2f})'.format(default))

args = parser.parse_args()
"""
#if (args.redo_file):
#connect to database and retrieve atoms object
db = connect("sub_100_Al-relaxed.db")
#sub_100_ids=[2, 3, 6, 7, 8, 10]

sub_100_ids = [args.ID]
k = args.kpt
#else: 
#    calc = GPAW('GPAW_ID_'+str(args.ID)+'_k:'+str(args.kpt)+'.gpw')


for cluster in db.select():
	atoms = cluster.toatoms()
        N_atoms = len(atoms)
        calc = GPAW(mode=PW(300),
            xc='PBE',
            kpts=(k, k, k),
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
