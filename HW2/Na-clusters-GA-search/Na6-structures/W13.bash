#!/usr/bin/env bash
#SBATCH -p hebbe 
#SBATCH -A C3SE2021-1-15 # Project
#SBATCH -J test # Name of the job
#SBATCH -N 1 # Use 1 node
#SBATCH -n 1 # Use only 1 core on that node
#SBATCH -t 01:00:00 # Maximum time
#SBATCH -o stdout # stdout goes to this file
#SBATCH -e stderr # stderr goes to this file
module purge
module load Python/3.7.4 Tkinter/3.7.4 intel/2019a ASE GPAW

echo "Starting T8 script at" $(date +"%I:%M:%S") >> Done.txt
mpirun python T8.py --hval 0.5 half-decahedron.db fd 

echo "runing completed at" $(date +"%I:%M:%S") >> Done.txt
