import numpy as np
import matplotlib.pyplot as plt

from ase import atoms
from ase.db import connect
from ase.io import write, read, Trajectory, iread
from ase.units import fs, kB
from ase.md.npt import NPT

from gpaw import GPAW
filename = 'cluster24wNa.traj'

atomic_numbers = read(filename).get_atomic_numbers()
#print(atomic_numbers == 8)
boolean_indices_O = (atomic_numbers == 8)
boolean_indices_H = (atomic_numbers == 1)

number_of_frames = 0
skip_frames = 1000
bins = 500
RDF = np.zeros(bins);
RDF_O = np.zeros(bins);
RDF_H = np.zeros(bins);

zero_array = np.zeros(bins, dtype = bool)

number_of_frames = 0
for atoms in iread('cluster24wNa.traj'):
    number_of_frames += 1
    #print("oxygen distances \n")
    #print(atoms.get_distances(72,boolean_indices_O))
    #print("Hydrogen distances \n")
    #print(atoms.get_distances(72,boolean_indices_H))
    #print("\n")
    #Compute RDF for all atoms, only Oxygen and only Hydrogen
    for index in range(np.sum(boolean_indices_O)):
        if(number_of_frames > skip_frames):
            RDF += np.histogram(atoms.get_distances(index,np.concatenate(zero_array[:index],boolean_indices_O[index:])),bins = bins, range = (0, 10), density = True)[0]

#print(RDF/number_of_frames)
#plt.plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF/(number_of_frames-skip_frames))
#plt.grid(True)
"""
fig = plt.figure()
axs = fig.add_subplots(figsize = (10,10))
axs.grid(True);
axs.set_xlabel('R [Å]');
axs.plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF/(number_of_frames-skip_frames),label = 'RDF total')
axs.legend();
plt.savefig('RDFO.png')

RDF_integral = 0
RDF_bins = np.histogram_bin_edges(atoms, bins = bins, range = (0,10))

for i in range(bins):
    RDF_integral += RDF[i]/(number_of_frames-skip_frames)*(10/bins)

print("\n total")
print(RDF_integral)
"""
