import time
start_time = time.time()

from random import random
from ase.io import write
from ase.db import connect
from ase.optimize import GPMin
from gpaw import GPAW, FermiDirac

from ase.ga.data import DataConnection
from ase.ga.population import Population
from ase.ga.standard_comparators import InteratomicDistanceComparator
from ase.ga.cutandsplicepairing import CutAndSplicePairing
from ase.ga.utilities import closest_distances_generator
from ase.ga.utilities import get_all_atom_types
from ase.ga.offspring_creator import OperationSelector
from ase.ga.standardmutations import MirrorMutation
from ase.ga.standardmutations import RattleMutation
from ase.ga.standardmutations import PermutationMutation
import argparse

parser = argparse.ArgumentParser()
defval = 0.3
parser.add_argument('-m', '--mutation_probability', type=float, default=defval,
                    help='Mutation probability (default: {:.2f})'.format(defval))
defval = 80
parser.add_argument('-n', '--ncandidates_to_test', type=int, default=defval,
                    help='Number of candidates to test (default: {})'.format(defval))
args = parser.parse_args()

# Initialize the different components of the GA
da = DataConnection('gadb.db')

# Determine size of starting population
db = connect('gadb.db')
population_size = db.count('natoms>0')
print('Running with population_size = {}'.format(population_size))

atom_numbers_to_optimize = da.get_atom_numbers_to_optimize()
n_to_optimize = len(atom_numbers_to_optimize)
slab = da.get_slab()
all_atom_types = get_all_atom_types(slab, atom_numbers_to_optimize)
blmin = closest_distances_generator(all_atom_types,
                                    ratio_of_covalent_radii=0.8)

comp = InteratomicDistanceComparator(n_top=n_to_optimize,
                                     pair_cor_cum_diff=0.015,
                                     pair_cor_max=0.7,
                                     dE=0.02,
                                     mic=False)


pairing = CutAndSplicePairing(slab, n_to_optimize, blmin)
mutations = OperationSelector([1., 1., 0.],
                              [MirrorMutation(blmin, n_to_optimize),
                               RattleMutation(blmin, n_to_optimize),
                               PermutationMutation(n_to_optimize)])


# Define the calculator
calc = GPAW(nbands=10,
            h=0.25,
            txt='out.txt',
            occupations=FermiDirac(0.05),
            setups={'Na': '1'},
            mode='lcao',
            basis='dzp')


# Relax all unrelaxed structures (e.g. the starting population)
while da.get_number_of_unrelaxed_candidates() > 0:
    a = da.get_an_unrelaxed_candidate()
    a.set_calculator(calc)
    print('Relaxing starting candidate {0}'.format(a.info['confid']))
    dyn = GPMin(a, trajectory='relax_ref.traj', logfile='relax_ref.log')
    dyn.run(fmax=0.02, steps=100)
    a.info['key_value_pairs']['raw_score'] = -a.get_potential_energy()
    da.add_relaxed_step(a)

# create the population
population = Population(data_connection=da,
                        population_size=population_size,
                        comparator=comp)

# test new candidates
for i in range(args.ncandidates_to_test):
    print('Now starting configuration number {}'.format(i))
    a1, a2 = population.get_two_candidates()
    a3, desc = pairing.get_new_individual([a1, a2])
    if a3 is None:
        continue
    da.add_unrelaxed_candidate(a3, description=desc)

    # Check if we want to do a mutation
    if random() < args.mutation_probability:
        a3_mut, desc = mutations.get_new_individual([a3])
        if a3_mut is not None:
            da.add_unrelaxed_step(a3_mut, desc)
            a3 = a3_mut

    # Relax the new candidate
    a3.set_calculator(calc)
    dyn = GPMin(a3, trajectory='relax_new.traj', logfile='relax_new.log')
    dyn.run(fmax=0.02, steps=100)
    a3.info['key_value_pairs']['raw_score'] = -a3.get_potential_energy()
    da.add_relaxed_step(a3)
    population.update()

write('all_candidates.traj', da.get_all_relaxed_candidates())


print("--- {:1f} seconds ---".format(time.time() - start_time))