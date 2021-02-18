

atoms = read('christmas-tree.xyz')
calc = GPAW(
	mode = 'fd',
	xc = 'LDA',
	setups = {'Na': '1'},
	h = 0.3,
	nbands = 0,
	txt = 'f.gpaw-out',
	)	
atoms.center(vacuum=8)
atoms.set_calculator(calc)
atoms.get_potential_energy()

calc.write('myCalc.gpw', 'all')
