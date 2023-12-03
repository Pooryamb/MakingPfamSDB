#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00           # time (DD-HH:MM)
#SBATCH --output=logs/slurm-ChopStructs_%A_%a.out

set -e

python Concat_ChoppedAndRemoveExtra.py

