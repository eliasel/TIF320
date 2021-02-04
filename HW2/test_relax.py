import time
start_time = time.time()

from gpaw import GPAW, FermiDirac

from ase.db import connect
from ase.ga.data import DataConnection
from ase.ga.population import Population
from ase import Atoms
from ase.ga.data import PrepareDB
from ase.optimize import GPMin
from ase.optimize import BFGS
from ase.calculators.lj import LennardJones 
#cluster = Atoms(Na)

#da = DataConnection('test.db')
#db = connect('test.db')

calc = GPAW(nbands=10,
	    h=0.25,
	    txt ='out.txt',
	    occupations=FermiDirac(0.05),
	    setups={'Na': '1'},
	    mode='lcao',
	    basis = 'dzp')

calc_lj = LennardJones(epsilon=0.46252798, sigma = 2.57488462)
cluster = Atoms('Na4', [(1.0,0,0), (0,1.0,0), (0,0,1.0), (1.0,1.0,0)])
"""
cluster = Atoms('Na',[(2.0,1.0,1.0)])
cluster = Atoms('Na',[(1.0,2.0,1.0)])
cluster = Atoms('Na',[(1.0,1.0,2.0)])
cluster = Atoms('Na',[(2.0,2.0,2.0)])
cluster = Atoms('Na',[(4.0,4.0,4.0)])
cluster = Atoms('Na',[(1.0,1.0,1.0)])
cluster = Atoms('Na',[(4.0,1.0,1.0)])
cluster = Atoms('Na',[(1.0,4.0,1.0)])
"""


cluster.set_cell([20,20,20])
cluster.set_calculator(calc_lj)

dyn = BFGS(cluster, trajectory = None, logfile = 'qn.log')
dyn.run(fmax = 0.05, steps = 1000)

cluster.set_calculator(calc_lj)

dyn2 = GPMin(cluster, trajectory = 'relax_ref.traj', logfile = 'relax_ref.log')
dyn2.run(fmax=0.02, steps = 100)
energy = cluster.get_potential_energy()
#atoms.calc = calc
#calc.write('Na4.gpw', mode = 'all')
