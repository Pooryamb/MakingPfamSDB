#!/bin/bash

set -e
mkdir -p logs
mkdir -p tmp

TMP="./tmp"

bash GetAllUnipStructsInAlphaDB.sh $TMP

wget -P $TMP https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.seed.gz

zcat ${TMP}/Pfam-A.seed.gz | ./ProcessSeeds.py

python FindAF_SeedsOverlap.py $TMP

python GetOneLineDescOfPfamSeeds.py $TMP

python ConvertUnipID2LinkAndGetReadyForDownloading.py $1 $TMP
