#!/usr/bin/env python3

#This is for getting the UnipID and locations of domains
#Of pfam seeds. It will also store their sequence
import sys


sys.stdin.reconfigure(encoding='latin-1')
input_file = sys.stdin
tmp = "./tmp"


outputFile = open(f"{tmp}/PfamSeedsTwoIDsAndLocs.tsv", 'w')
PfamSeedsFastaFile = open(f"{tmp}/PfamSeeds.fasta",'w')
JustIDs = open(f"{tmp}/JustIDsOfSeeds.csv",'w')
pfamseqid = open(f"{tmp}/pfamseqid.csv", 'w')

PF = ""

IDsList = []
pfamseq_ids = []
for line in input_file:
    if line.startswith("#=GF AC"):
        PF = line.strip().split()[-1].split(".")[0]
        NameDict = {}
    elif line.startswith("#=GS "):
        if line.split()[2]=="AC":
            UnipID = line.strip().split()[-1].split(".")[0]
            pfamseq_id = line.strip().split()[-1]
            IDsList.append(UnipID)
            pfamseq_ids.append(pfamseq_id)
            Start, End = line.split()[1].split("/")[1].split("-")
            LongName = line.split()[1]
            NewDesig = "_".join([UnipID, Start, End, PF])
            NameDict[LongName] = NewDesig
            outputFile.write("\t".join([UnipID, Start, End, PF, LongName]) + "\n")
    elif line[0].isalnum():
        LongName = line.split()[0]
        Seq = line.split()[1]

        PfamSeedsFastaFile.write(">" + NameDict[LongName] + "\n" + Seq.strip().replace(".",'').upper() + "\n")

JustIDs.write("\n".join(sorted(list(set(IDsList)))))
pfamseqid.write("\n".join(sorted(list(set(pfamseq_ids)))))
pfamseqid.close()
JustIDs.close()
PfamSeedsFastaFile.close()
outputFile.close()
