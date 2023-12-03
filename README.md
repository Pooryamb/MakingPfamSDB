This GitHub repository is for making the Pfam seeds structure database (PfamSDB) by cutting the related full-length 
structures on their domain borders. 
Prerequisites:
* python
* pandas
* gsutil (It is assumed that you have access to the Alphafold database)
* GNU parallel
* seqtk
* Biopython
* foldseek (For cutting the Foldseek database on domain borders)

This script was run on a machine with SLURM job scheduler. It uses job arrays to download structures 
and cut them in parallel.

It can be run as follows:

```
cd scripts
batch=32 #We will cut structures in batches. You can specify the number of batches here.
bash Prepare2DownloadStructs.sh $batch 
sbatch --array=1-$batch DownloadTarStructsAndExtractFasta.sh
bash Prepare2ChopStructs.sh
sbatch --array=1-$batch RunCifChopper.sh
python Concat_ChoppedAndRemoveExtra.py
```

The PfamSDB will be inside the structures directory.

If you are interested in cutting the Foldseek database on domain borders, run the following command in the end:
```
bash MakeFScutDB.sh
```
The PfamSDB made by cutting the Foldseek database would be in "PfamSDB_fscut" directory.
