from ase.db import connect
from ase.io import write
from ase.units import fs, kB


atoms = read('NaH20.xyz')

calc = GPAW(
            mode = 'lcao',
            xc = 'PBE',
            basis = 'dzp',
            symmetry = {point_group = False},
            charge = 1,
            txt = 'GPAW_output.gpaw-out')

atoms.set_calculator(calc)

dyn = NPT(atom
            temperature = 350*kB,
            timestep = 0.5*fs,
            ttime = 20*fs,
            logfile = 'MDout.log')

traj = Trajectory('cluster24wNa.tradj','w',atoms)
dyn.attach(traj.write, interval = 1)

dyn.run(10)


"""lowest_energy = 0
lowest_id = 0
db = connect('gadb.db')

for row in db.select():
  atoms = row.toatoms()
  print(atoms.calc.)
  if(atoms.calc != None):
    current_energy = row.energy
    if current_energy<lowest_energy:
      lowest_energy = current_energy
      lowest_id = row.id

atoms = db.get(id=lowest_id).toatoms()
print(atoms)

print(atoms.get_total_energy())
write('ground_states.xyz', atoms)

"""
