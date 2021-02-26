from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations

#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
#sub_100_ids=[2, 3, 6, 7, 8, 10]

All_ids = [1,2,3,4,5,6,7,8,9,10]
k = 4

for id in sub_100_ids:
#while (i == 1):
#    cluster = db[2]
    calc = GPAW(mode=PW(300),
                xc='PBE',
                kpts=(k, k, k),
                random=True,  # random guess (needed if many empty bands required)
                occupations=FermiDirac(0.01),
                txt='id_'+str(id)+'_gs.txt')

    cluster = db.select(id = id)
    atoms = cluster.toatoms()
    N_atoms = len(atoms)

    atoms.calc = calc
    BFGS(atoms).run(fmax=0.01)
    write('Al-relaxed.db', atoms, append = True)


#db.write(atoms, data = {'frequency' : freq, 'density-of-states' : dos})
