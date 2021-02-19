import matplotlib.pyplot as plt
from gpaw.lrtddft import LrTDDFT
from gpaw.lrtddft.spectrum import get_folded_spectrum

lr = LrTDDFT('Na_110.gz') 

x,y = get_folded_spectrum(lr, width = 0.06)
fig, ax = plt.subplots()
plt.plot(x, y[:,0])
ax.set_xlabel('energy [eV]')
plt.savefig('./spectrum_T1.pdf')
