#It is for getting a list of Uniprot IDs and then Downloading them all from UniProt DB
# It has not been used in this repository
import os
import glob
import sys
import pandas as pd

tmp=sys.argv[1]

PfamCordsPath = f"{tmp}/PfamCordsOnSeedsOneLineFormatAFadj.tsv"

AllCords = pd.read_csv(PfamCordsPath, sep="\t", header=None)

Batches = glob.glob("../structures/B*_list.txt")
for Batch in Batches:
    BatchProts = pd.read_csv(Batch, header=None)
    BatchProts[0] = BatchProts[0].str.replace(".cif.gz", "")
    BatchCords = BatchProts.merge(AllCords, on = 0, how = "left")
    BatchCords.to_csv(tmp + "/" + os.path.basename(Batch).replace("_list.txt", "_Cords.txt"), sep="\t", header=None, index=None)

