from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations

#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
#sub_100_ids=[2, 3, 6, 7, 8, 10]

sub_100_ids = [2]
k = 4

calc = GPAW(mode=PW(300),
            xc='PBE',
            kpts=(8, 8, 8),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.01))

for id in sub_100_ids:
#while (i == 1):
#    cluster = db[2]
    cluster = db.select(id = id)
    atoms = cluster.toatoms()
    N_atoms = len(atoms)

    atoms.calc = calc
    BFGS(atoms).run(fmax=0.01)
    vib = Vibrations(atoms)
    vib.clean()
    vib.run()
    vib.summary()
    vib.write_dos(out='vib-dos'+str(i)+'.dat')
    freq = vib.get_frequencies()
#print(vib.get_mode(1))
#print(freq)
#print(len(freq))
    i=i+1
    energies = vib.get_energies()
    #print(energies)
    vib.clean()


#db.write(atoms, data = {'frequency' : freq, 'density-of-states' : dos})
