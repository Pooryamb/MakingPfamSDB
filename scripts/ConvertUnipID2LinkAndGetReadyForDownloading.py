#This script starts from a list of Uniprot IDs, creates their downloadable links 
#and makes the related directories.
import os
import sys
from math import ceil


NumOfBatch = int(sys.argv[1])
tmp = sys.argv[2]

count = sum(1 for _ in open(f"{tmp}/SeedAFIntersection.tsv"))
file = open(f"{tmp}/SeedAFIntersection.tsv")

os.system("mkdir -p ../structures")
out = open("../structures/B1_links.txt", 'w')


batch = ceil(count/NumOfBatch)
counter = 0
for line in file:
    ID = line.strip()
    out.write("gs://public-datasets-deepmind-alphafold-v4/AF-" + ID + "-*_v4.cif\n")
    counter += 1
    if counter%batch==0:
        out.close()
        batchNum = counter//batch + 1
        out = open("../structures/B" + str(batchNum) + "_links.txt", 'w')
        
for i in range(1,batchNum+1):
    os.system("mkdir -p ../structures/B" + str(i))
out.close()
file.close()
