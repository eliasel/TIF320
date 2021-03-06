from ase.build import bulk
from ase.calculators.emt import EMT
from ase.phonons import Phonons
import numpy as np

# Setup crystal and EMT calculator
atoms = bulk('Al')

# Phonon calculator
N = 7
ph = Phonons(atoms, EMT(), supercell=(N, N, N), delta=0.05)
ph.run()

# Read forces and assemble the dynamical matrix
ph.read(acoustic=True)
ph.clean()

path = atoms.cell.bandpath('GXULGK', npoints=100)
#print(path.kpts)
print(atoms.cell.reciprocal()[0][0])
bs = ph.get_band_structure(path)
#print(bs.energies)
#print(bs.energies[0,5][2])
#print(path.kpts[5,1])

#241.79893 eV to THz
k_vec = np.sqrt(path.kpts[:,0]**2+path.kpts[:,1]**2+path.kpts[:,2]**2)
k_vec = np.sqrt(3)*np.abs(atoms.cell.reciprocal()[0][0])*k_vec #All entries are the same in reciprocal
print('Speed velocity [m/s]: ' + str(241.79893*10**2*bs.energies[0,5][0]/k_vec[5]))
print('Speed velocity [m/s]: ' + str(241.79893*10**2*bs.energies[0,5][2]/k_vec[5]))


dos = ph.get_dos(kpts=(20, 20, 20)).sample_grid(npts=100, width=1e-3)

# Plot the band structure and DOS:
import matplotlib.pyplot as plt  # noqa
fig = plt.figure(1, figsize=(7, 4))
ax = fig.add_axes([.12, .07, .67, .85])

emax = 0.035
bs.plot(ax=ax, emin=0.0, emax=emax)

"""
dosax = fig.add_axes([.8, .07, .17, .85])
dosax.fill_between(dos.weights[0], dos.energy, y2=0, color='grey',
                   edgecolor='k', lw=1)

dosax.set_ylim(0, emax)
dosax.set_yticks([])
dosax.set_xticks([])
dosax.set_xlabel("DOS", fontsize=18)
"""

fig.savefig('Al_phonon.png')
