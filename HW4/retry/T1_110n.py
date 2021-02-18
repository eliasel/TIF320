from ase import atoms
from ase.io import read, write
from gpaw import GPAW

# Reload ground state from before to
calc = GPAW("gsNa8.gpw")
calc.get_eigenvalues()
calc.get_occupation_numbers()

atoms = calc.get_atoms()
#atoms.get_potential_energy() # Performs the calculation on the system !

calc.set(
nbands = 110,           #
convergence = {"bands": -10},# Do not converge final 10 states
fixdensity = True,      # Keep density constant in calculations
txt = "Na_n110.gpaw-out"     # Redirect GPAW ’s text output to f.gpaw - out
)
atoms.get_potential_energy() # Performs the calculation on the system !

#Save the new ground state to a file
calc.write("Na_110n.gpw", "all") # Writes everything it can to file !
