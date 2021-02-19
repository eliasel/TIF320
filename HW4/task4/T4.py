from ase import atoms
from ase.io import read, write
from gpaw import GPAW
from gpaw.tddft import *

# Reload ground state from before to
calc = TDDFT("gsNa8.gpw")

time_step = 30.0                  # 1 attoseconds = 0.041341 autime
iterations = 1500                # 1500 x 30 as => 45 fs
kick_strength = [0.0,0.0,1e-5]   # Kick to z-direction

# Kick with a delta pulse to z-direction
td_calc.absorption_kick(kick_strength=kick_strength)

# Propagate, save the time-dependent dipole moment to 'be_dm.dat',
# and use 'be_td.gpw' as restart file
td_calc.propagate(time_step, iterations, 'be_dm.dat', 'be_td.gpw')

# Calculate photoabsorption spectrum and write it to 'be_spectrum_z.dat'
photoabsorption_spectrum('be_dm.dat', 'be_spectrum_z.dat', width = 0.06)
