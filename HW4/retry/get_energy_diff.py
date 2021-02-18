from ase import atoms
from ase.io import read, write
from gpaw import GPAW
from gpaw.lrtddft import LrTDDFT, photoabsorption_spectrum

# Reload ground state from before to
calc = GPAW("Na_110n.gpw")
#calc = GPAW("gsNa8.gpw")
print(calc.get_eigenvalues())

dE = 6  # maximal Kohn-Sham transition energy to consider in eV
lr = LrTDDFT(calc,
		xc='LDA',
		energy_range = dE,
		)
lr.write('Na_110.gz')

lr = LrTDDFT.read('Na_110.gz')
lr.diagonalize()

# write the spectrum to the data file
photoabsorption_spectrum(lr,
                         'spectrum_w.05eV.dat',  # data file name
                         width=0.06)             # width in eV

lr.write('LrTDDFTresults.dat') # Save for task 2
