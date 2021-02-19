from ase import atoms
from ase.io import read, write
from gpaw import GPAW
from gpaw.tddft import *

# Reload ground state from before to
calc = TDDFT("gsNa8.gpw")

time_step = 30.0                  # 1 attoseconds = 0.041341 autime
iterations = 1500                # 1500 x 30 as => 45 fs
kick_strength = [1e-5,0.0,0.0]   # Kick to x-direction

# Kick with a delta pulse to z-direction
calc.absorption_kick(kick_strength=kick_strength)

# Propagate, save the time-dependent dipole moment to 'be_dm.dat',
# and use 'be_td.gpw' as restart file
calc.propagate(time_step, iterations, 'be_dm_x.dat', 'be_td_x.gpw')

# Calculate photoabsorption spectrum and write it to 'be_spectrum_x.dat'
photoabsorption_spectrum('be_dm_x.dat', 'be_spectrum_x.dat', width = 0.06)
