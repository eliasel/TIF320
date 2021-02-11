from ase import atoms
from ase.db import connect
from ase.io import write, read, Trajectory
from ase.units import fs, kB
from ase.md.npt import NPT

from gpaw import GPAW


traj = read('cluster24wNa.traj')

print(traj.get_distances())
