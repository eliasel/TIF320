from ase import atoms
from ase.io import read, write
from gpaw import GPAW


atoms = read("someAtomsFromSomewhere.xyz")
atoms.center(vacuum=8)  # apply 8 Å of vacuum around atoms

calc = GPAW (
mode ="fd",           # Use the finite - difference mode
xc = "LDA",            # Use LDA exchange - correlation
setups = {"Na": '1'},  # Use a single - valence electron setup
h = 0.3 ,               # Grid spacing
nbands = 0,             # Include only occupied states
txt = "T1_createGS.gpaw-out"   # Redirect GPAW ’s text output to f.gpaw - out
)

atoms.set_calculator(calc)
atoms.get_potential_energy() # Performs the calculation on the system !

#Save first ground state with only one valence electron
calc.write("gsNa8.gpw", "all") # Writes everything it can to file !
