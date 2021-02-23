import matplotlib.pyplot as plt
from gpaw.lrtddft import LrTDDFT
from gpaw.lrtddft.spectrum import get_folded_spectrum

lr = LrTDDFT('LrTDDFTresults.dat') 
lr.diagonalize(energy_range=4) 

x,y = get_folded_spectrum(lr, width = 0.06)
fig, ax = plt.subplots()
plt.plot(x, y[:,0])
ax.set_xlabel('energy [eV]')
ax.set_ylabel('Folded oscillation strength')
plt.savefig('./spectrum_T5.pdf')
