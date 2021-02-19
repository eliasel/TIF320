import numpy as np
from scipy.linalg import eig
import matplotlib.pyplot as plt


dump = np.load('dumpsterboi.dump.npz')
K_pp = dump['K_pp']
w_p=dump['ediff_p']
i_p = dump['i_p']
a_p = dump['a_p']
mux_p = dump['mux_p']
muy_p = dump['muy_p']
muz_p = dump['muz_p']


#calc = GPAW('calc.gpaw', 'all')
N = len(w_p)

Omega = np.zeros((N,N))
for i in range(N):
	Omega[i,i] = w_p[i]**2

for p in range(N):
	for q in range(N):
		n_p = a_p[p]-i_p[p]
		n_q = a_p[q]-i_p[q]
		Omega[p,q] = 2*np.sqrt(w_p[p]*n_p)*K_pp[p,q]*np.sqrt(w_p[q]*n_q)

[omega2, FI] = eig(Omega)
idx = omega2.argsort()[::-1]
omega2 = omega2[idx]
FI = FI[:,idx]

fz_I = np.zeros(N)
for I in range(N):
	for p in range(N):
		FI_p = FI[:, I]
		fz_I[I] = fz_I[I] + 2*np.abs(np.sqrt(w_p[p]*(a_p[p]-i_p[p]))*muz_p[p]*FI_p[p])




def fold(x_t, x_i, y_i, width):
    '''
        Convolutes each peak in the discrete spectrum
        with a Gaussian of chosen width.
        
        inputs:
        x_t:    vector with energies (i.e. linspace/np.arange)
        x_i:    stick spectrum energies
        y_i:    stick spectrum intensities
        width:  width of the Gaussian

        outputs:
        y_t:    convoluted spectrum, i.e. intensities
    '''
    def Gauss(x0):
        norm = 1.0 / (width * np.sqrt(2 * np.pi))
        return norm * np.exp(-0.5 * (x_t - x0)**2 / width**2)

    y_t = np.zeros_like(x_t)
    for x, y in zip(x_i, y_i):
        y_t += y * Gauss(x)
    return y_t

x_t = np.linspace(-1, 3, N, dtype = 'complex')
y_t = fold(x_t, np.sqrt(omega2), fz_I, 0.06)

fig, ax = plt.subplots()
ax.plot(x_t, y_t)
ax.set_xlabel('Energies [eV]')
ax.set_ylabel('Intensity []')
fig.savefig('./spectrum_T2.pdf')
		
 
