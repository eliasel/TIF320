from ASE.calculator.eam import EAM
from ase.db import connect 

mishim = EAM(potentail='al_potential.alloy')
mishim.plot()

db = connect('Al-clusters.db')
atoms = db[1].toatoms()

atoms.calc = mishim
atoms.get_potential
atoms.get_forces

mishim.write("Al-cluster.gpw", "all")
