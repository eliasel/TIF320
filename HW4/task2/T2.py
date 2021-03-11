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
fdiff_p = dump['fdiff_p']

#calc = GPAW('calc.gpaw', 'all')
#from gpaw.lrtddft import LrTDDFT
N = len(w_p)

Omega = np.zeros((N,N))
for i in range(N):
	Omega[i,i] = w_p[i]**2

for p in range(N):
	for q in range(N):
		n_p = a_p[p]-i_p[p]
		n_q = a_p[q]-i_p[q]
		Omega[p,q] = Omega[p,q] + 4.0*np.sqrt(w_p[p])*K_pp[p,q]*np.sqrt(w_p[q])

[omega2, FI] = eig(Omega)
idx = omega2.argsort()[::-1]
omega2 = omega2[idx]
FI = FI[:,idx]

fx_I = np.zeros(N)
for I in range(N):
	for p in range(N):
		FI_p = FI[:, I]
		fx_I[I] = fx_I[I] + np.sqrt(w_p[p]*2.0)*mux_p[p]*FI_p[p]
 

fx_I = 2*np.abs(fx_I)**2

fy_I = np.zeros(N)
for I in range(N):
	for p in range(N):
		FI_p = FI[:, I]
		fy_I[I] = fy_I[I] + np.sqrt(w_p[p]*2.0)*muy_p[p]*FI_p[p]
 
fy_I = 2*np.abs(fy_I)**2


fz_I = np.zeros(N)
for I in range(N):
	for p in range(N):
		FI_p = FI[:, I]
		fz_I[I] = fz_I[I] + np.sqrt(w_p[p]*2.0)*muz_p[p]*FI_p[p]
                
fz_I = 2*np.abs(fz_I)**2

favr_I = (fx_I + fy_I + fz_I)/3

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
print(np.amax(w_p))
x_t = np.linspace(1, 6.5, N, dtype = 'complex')
eps_i = np.sqrt(omega2)*27.2107
y_t = fold(x_t, eps_i, favr_I, 0.06)


fig, ax = plt.subplots()
ax.plot(x_t, np.abs(y_t))
ax.set_xlabel('Energies [eV]')
ax.set_ylabel('Folded oscillator strength')
fig.savefig('./spectrum_T2.pdf')
		
 
