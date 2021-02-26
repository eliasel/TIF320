from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations

#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
i=1

for cluster in db.select():
#while (i == 1):
#    cluster = db[2]
    f = open('vib_spec_'+str(i)+'.txt','w')
    f.write('frequency [cm^-1], energy [eV]\n')
    atoms = cluster.toatoms()
#atoms = db[i].toatoms()
    N_atoms = len(atoms)
    atoms.calc = calc
    BFGS(atoms).run(fmax=0.01)
    vib = Vibrations(atoms)
    vib.clean()
    vib.run()
    vib.summary()
#vib.write_dos(out='vib-dos'+str(i)+'.dat')
    freq = vib.get_frequencies()
#print(vib.get_mode(1))
    #print(freq)
#print(len(freq))
    i=i+1
    energies = vib.get_energies()
    #print(energies)
    print(len(freq))
    for j in range(len(freq)):    
        f.write(f'{freq[j]}, {energies[j]}\n')
    f.close()    
    vib.clean()


#db.write(atoms, data = {'frequency' : freq, 'density-of-states' : dos})
