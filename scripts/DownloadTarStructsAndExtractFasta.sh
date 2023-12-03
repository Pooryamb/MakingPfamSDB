#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --cpus-per-task=4
#SBATCH --time=17:00:00           # time (DD-HH:MM)
#SBATCH --output=logs/slurm-DownloadAndTar_%A_%a.out

set -e

cd ../structures/
batch=B$SLURM_ARRAY_TASK_ID

cat ${batch}_links.txt | gsutil -m cp -I ./${batch}

cd $batch
find . -type f -name "*-F1-model_v4.cif" | parallel 'mv {} `echo {} | sed "s/-F1-model_v4//"`'
find . -type f -name "AF-*" | parallel 'mv {} `echo {} | sed "s/AF-//"`'

ls | parallel 'gzip {}'

tar -cf ${batch}.tar * 
mv ${batch}.tar ..
ls | parallel 'rm {}'

cd ../
rm -r ${batch}

python ../scripts/ExtractFastaFromTar.py ${batch}.tar

tar -tf ${batch}.tar > ${batch}_list.txt
