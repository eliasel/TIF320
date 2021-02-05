from ase.db import connect
import numpy as np
from ase.io import write
base_name = 'Na8'

db = connect('gadb.db')
#db = db.get(id=129, sort='energy').energy
#atom = db.get('id=1').toatoms()
Energies = np.zeros((2,100))
i=0
for row in db.select(calculator = 'gpaw'):
	Energies[0,i]=row.energy
	Energies[1,i]=row.id
	i=i+1
E_ind = np.argmin(Energies[0,:])
E_low_id=np.int(Energies[1,E_ind])
cluster = db.get(id=E_low_id).toatoms(attach_calculator=True)
calc = cluster.calc

energy = cluster.get_potential_energy()
nbands = calc.get_number_of_bands()
for band in range(nbands):
	wf = calc.get_pseudo_wave_function(band=band)
	fname = f'{base_name}_{band}.cube'
	write(fname, cluster, data=wf)
	print(band)
print('Hej, hej hej--------------------')
print(E_low_id)
print('Hej, hej hej--------------------')
