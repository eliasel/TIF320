from ase import atoms
from ase.io import read, write
from ase.db import connect
from ase.calculators.eam import EAM
from ase.optimize import BFGS
from ase.vibrations import Vibrations
import matplotlib.pyplot as plt

#connect to database and retrieve atoms object
db = connect("Al-clusters-initial.db")
calc = EAM(potential = 'al_potential.alloy')
i=1
for cluster in db.select():
    atoms = cluster.toatoms()
    #atoms = db[i].toatoms()
    No_atoms = len(atoms)
    atoms.calc = calc
    #BFGS(atoms).run(fmax=0.01)
    vib = Vibrations(atoms)
    vib.run()
    vib.summary()
    freq = vib.get_frequencies()
    vib.clean()
    db.write(atoms, data = {'frequency' : freq})
    #print(freq)
    #print(len(freq))


    fig, ax = plt.subplots()
    N_mode = range(len(freq))
    ax.plot(N_mode, freq)
    ax.set_xlabel('Mode nr')
    ax.set_ylabel('Frequency [cm^-1]')
    fig.savefig('./plots/freq_mode'+str(i)+'.pdf')

    fig, ax = plt.subplots()
    ax.hist(freq, bins = 20)
    ax.set_xlabel('Frequency [cm^-1]')
    ax.set_ylabel('DOS')
    fig.savefig('./plots/dos' + str(i)+'.pdf')
    
    i=i+1

#vib.write_dos(out='vib-dos'+str(i)+'.dat')
#print(vib.get_mode(1))
#print(freq)
#print(len(freq))
#i=i+1



