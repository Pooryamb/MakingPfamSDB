#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00           # time (DD-HH:MM)
#SBATCH --output=logs/slurm-ChopStructs_%A_%a.out

set -e

batch=B$SLURM_ARRAY_TASK_ID

python CifChopperHandler.py ../structures/${batch}.tar ./tmp/${batch}_Cords.txt

## Sometimes, the tar file made by python is not parsable by Foldseek. The following parts extract the Tar file and retar the PDB files using Tar instead of python
mkdir ../structures/${batch}
cd ../structures/${batch}
mv ../${batch}_chopped.tar .
tar -xf ${batch}_chopped.tar
tar -cf ../${batch}_chopped.tar *.pdb.gz
rm *.pdb.gz
cd ..
rm -r ${batch}
cd ../scripts
