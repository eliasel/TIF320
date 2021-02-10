from ase import atoms
from ase.db import connect
from ase.io import write, read, Trajectory
from ase.units import fs, kB
from ase.md.npt import NPT

from gpaw import GPAW


atoms = read('NaH2O.xyz')

calc = GPAW(
            mode = 'lcao',
            xc = 'PBE',
            basis = 'dzp',
            symmetry = {'point_group': False},
            charge = 1,
            txt = 'GPAW_output.gpaw-out')

atoms.set_calculator(calc)

dyn = NPT(atoms,
	0.5*fs,
	temperature = 350*kB,
	ttime = 20*fs,
	logfile = 'MDout.log',
	externalstress = 0,
	pfactor = None)
	
traj = Trajectory('cluster24wNa.traj','w',atoms)
dyn.attach(traj.write, interval = 1)

f = open("Calclog.txt", "a")
for i in range(200):
  f.write(f"Running calculation, first {(i+1)*20*0.5} fs \n")
  dyn.run(20)
  

