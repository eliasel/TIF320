
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("energy_v_lattice.txt", delimiter =',', skip_header = 1)

fig = plt.figure(figsize = (8,5))
ax = fig.add_subplot(1, 1, 1)
ax.plot(data[:,0],data[:,1], label = 'energy vs Lattice parameter')
ax.annotate(f'min x:{data[np.argmin(data[:,1]),0]}, y:{np.min(data[:,1])}',(data[np.argmin(data[:,1]),0],np.min(data[:,1])))
#ax.grid(True)
ax.set_xlabel("Lattice parameter")
ax.set_ylabel("Energy [eV]")
fig.savefig('Eva.png')
