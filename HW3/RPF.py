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


for atoms in iread('cluster24wNa.traj'):
    number_of_frames += 1
    #print("oxygen distances \n")
    #print(atoms.get_distances(72,boolean_indices_O))
    #print("Hydrogen distances \n")
    #print(atoms.get_distances(72,boolean_indices_H))
    #print("\n")
    #Compute RDF for all atoms, only Oxygen and only Hydrogen
    if(number_of_frames > skip_frames):
        RDF += np.histogram(atoms.get_distances(72,range(72)),bins = bins, range = (0, 10), density = True)[0]
        RDF_O += np.histogram(atoms.get_distances(72,boolean_indices_O),bins = bins, range = (0, 10), density = True)[0]
        RDF_H += np.histogram(atoms.get_distances(72,boolean_indices_H),bins = bins, range = (0, 10), density = True)[0]

#print(RDF/number_of_frames)
#plt.plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF/(number_of_frames-skip_frames))
#plt.grid(True)

fig, axs = plt.subplots(3, 1,figsize = (10,10))
axs[0].grid(True);axs[1].grid(True);axs[2].grid(True)
axs[0].set_xlabel('R [Å]');axs[1].set_xlabel('R [Å]');axs[2].set_xlabel('R [Å]')
axs[0].set_ylabel('density [1/Å]');axs[1].set_ylabel('density [1/Å]');axs[2].set_ylabel('density [1/Å]');
axs[0].plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF/(number_of_frames-skip_frames),label = 'RDF total')
axs[1].plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF_O*24/(number_of_frames-skip_frames),label = 'RDF Oxygen')
axs[2].plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF_H*48/(number_of_frames-skip_frames),label = 'RDF Hydrogen')
axs[0].legend();axs[1].legend();axs[2].legend() 
axs[1].axvline(3);axs[2].axvline(4)
plt.savefig('RDF.png')

RDF_integral = 0
RDF_integral_O = 0
RDF_integral_H = 0
RDF_bins = np.histogram_bin_edges(atoms, bins = bins, range = (0,10))

for i in range(bins):
    if(RDF_bins[i] < 3):
        #RDF_integral += RDF[i]/(number_of_frames-skip_frames)*(10/bins)
        RDF_integral_O += RDF_O[i]/(number_of_frames-skip_frames)*(10/bins)*24
    if(RDF_bins[i] < 4):
        RDF_integral_H += RDF_H[i]/(number_of_frames-skip_frames)*(10/bins)*48

print("\n total")
print(RDF_integral)
print("\n Oxygen")
print(RDF_integral_O)
print("\n Hydrogen")
print(RDF_integral_H)
