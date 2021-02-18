import numpy as np
import matplotlib.pyplot as plt

from ase import atoms
from ase.db import connect
from ase.io import write, read, Trajectory, iread
from ase.units import fs, kB
from ase.md.npt import NPT

from gpaw import GPAW
filename = 'cluster24.traj'

atomic_numbers = read(filename).get_atomic_numbers()
boolean_indices_O = (atomic_numbers == 8)
boolean_indices_H = (atomic_numbers == 1)

number_of_frames = 0
skip_frames = 1000
bins = 500
RDF = np.zeros(bins);
Rmax = 13
zero_array = np.zeros(bins, dtype = bool)

for atoms in iread(filename):
    number_of_frames += 1
    #print("oxygen distances \n")
    #print(atoms.get_distances(72,boolean_indices_O))
    #print("Hydrogen distances \n")
    #print(atoms.get_distances(72,boolean_indices_H))
    #print("\n")
    #Compute RDF for all atoms, only Oxygen and only Hydrogen
    for index in range(np.sum(boolean_indices_O)-2):
        if(number_of_frames > skip_frames):
            RDF += np.histogram(atoms.get_distances(index,np.concatenate((zero_array[:index+1],boolean_indices_O[index+1:]))),bins = bins, range = (0, Rmax))[0]
#        if(number_of_frames == 1):
#            print(np.histogram(atoms.get_distances(index,np.concatenate((zero_array[:index+1],boolean_indices_O[index+1:]))),bins = bins, range = (0, 10), density = True)[0])

#print(RDF/number_of_frames)
#plt.plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF/(number_of_frames-skip_frames))
RDF = RDF/(np.sum(RDF)*Rmax/bins)*23
fig, ax = plt.subplots(figsize = (8,6))
ax.plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,Rmax)),RDF,label = 'RDF Oxygen')
ax.legend();
ax.set_xlim(2,6)
ax.grid(True);
ax.axvline(3.2)
ax.set_xlabel('R [Å]');
plt.savefig('RDFO.png')

RDF_integral = 0
RDF_bins = np.histogram_bin_edges(atoms, bins = bins, range = (0,Rmax))

for i in range(bins):
    if (RDF_bins[i] < 3.2):
        RDF_integral += RDF[i]

print("\n total")
print(RDF_integral*Rmax/bins)
