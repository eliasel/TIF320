from ase import atoms
from ase.io import read, write
from gpaw import GPAW

# Reload ground state from before to
calc = GPAW("Na_110n.gpw")
#calc = GPAW("gsNa8.gpw")
print(calc.get_eigenvalues())
