from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations

#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
i=2
#for cluster in db.select():
   # atoms = cluster.toatoms()
atoms = db[i].toatoms()
No_atoms = len(atoms)
atoms.calc = calc
BFGS(atoms).run(fmax=0.01)
vib = Vibrations(atoms)
vib.clean()
vib.run()
vib.summary()
#vib.combine()
vib.clean()
#vib.write_dos(out='vib-dos'+str(i)+'.dat')
freq = vib.get_frequencies()
print(vib.get_mode(1))
print(freq)
print(len(freq))
#i=i+1



db.write(atoms, data = {'frequency' : freq})
