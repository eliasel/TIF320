import numpy as np
from ase.db import connect

db = connect('Al-clusters-initial.db')
i=1
freq = db[i].data['frequency']
print(freq)
fig, ax = plt.subplots()
N_mode = range()
ax.plot(N_mode, freq)
ax.set_xlabel('Mode nr'))
ax.set_ylabel('Frequency [cm^-1]')
fig.savefig('./plots/freq_mode')

fig, ax = plt.subplots()
ax.hist(freq, bins = 20)
ax.set_xlabel('Frequency [cm^-1]'))
ax.set_ylabel('DOS')
fig.savefig('./plots/freq_mode')

