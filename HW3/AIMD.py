from ase.db import connect
from ase.io import write

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
