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

for atoms in iread('cluster24wNa.traj'):
    number_of_frames += 1
    #print("oxygen distances \n")
    #print(atoms.get_distances(72,boolean_indices_O))
    #print("Hydrogen distances \n")
    #print(atoms.get_distances(72,boolean_indices_H))
    #print("\n")
    if(number_of_frames > skip_frames):
        RDF += np.histogram(atoms.get_distances(72,range(72)),bins = bins, range = (0, 10), density = True)[0]
#print(RDF/number_of_frames)
plt.plot(np.histogram_bin_edges(atoms,bins=bins-1,range=(0,10)),RDF/(number_of_frames-skip_frames))
plt.grid(True)
plt.savefig('RDF.png')
RDF_integral = 0
RDF_bins = np.histogram_bin_edges(atoms, bins = bins, range = (0,10))

for i in range(bins):
    if(RDF_bins[i] < 3.3):
        RDF_integral += RDF[i]/(number_of_frames-skip_frames)*(10/bins)
print(RDF_integral*24)
