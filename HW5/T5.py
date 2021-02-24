from ase import atoms
from ase.db import connect
from ase.io import write, read
from ase.calculators.eam import EAM
from ase.dft.dos import DOS
#from gpaw import GPAW

db = connect('Al-clusters-initial.db')
calc = EAM(potential = 'al_potential.alloy')

#calc = EAM('al_potential.alloy')
#calc = GPAW(
#mode ='fd',
#xc = 'LDA',
#setups = {'Na':  '1'},
#nbands=0,
#txt='T5.gpaw-out'
#)

d = ()
e = ()
for cluster in db.select():
    atoms = cluster.toatoms()
    if atoms.get_global_number_of_atoms()<100.0:
        atoms.set_calculator(calc)
        pot_E = atoms.get_potential_energy()
        dos = DOS(calc)
        d = d + (dos.get_dos(),)
        e = e + (dos.get_energies(),)
