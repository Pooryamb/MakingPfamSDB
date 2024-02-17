#!/usr/bin/env python3

# This script will process the Pfam-A.seed.gz file.
# It would write the fasta file of the seeds, the UniProt ID of the seeds,
# The location of start and the end of the domain on each seed, and the UniProt ID+version.
import sys

sys.stdin.reconfigure(encoding='latin-1')
input_file = sys.stdin
tmp = "./tmp"

unipids_lst = []
unipids_ver_lst = []

with open(f"{tmp}/seeds_coords.tsv", 'w') as seed_coords_file, \
    open(f"{tmp}/unip_ids_pf.tsv", 'w') as seed_unipids_file, \
    open(f"{tmp}/seeds_seq.fasta", 'w') as seeds_seq_file, \
    open(f"{tmp}/unipver_ids_pf.tsv", 'w') as seed_unipver_ids_file :
    pfam_family = ""
    for line in input_file:
        if line.startswith("#=GF AC"):
            pfam_family = line.strip().split()[-1].split(".")[0]
            pfamnaming2newnaming = {}
            
        elif line.startswith("#=GS "):
            if line.split()[2]=="AC":
                seed_unipid = line.strip().split()[-1].split(".")[0]
                seed_unipid_ver = line.strip().split()[-1]
                unipids_lst.append(seed_unipid)
                unipids_ver_lst.append(seed_unipid_ver)
                seed_start, seed_end = line.split()[1].split("/")[1].split("-")
                seed_pfname = line.split()[1]
                seed_newname = "_".join([seed_unipid, seed_start, seed_end, pfam_family])
                pfamnaming2newnaming[seed_pfname] = seed_newname
                seed_coords_file.write("\t".join([seed_unipid, seed_start, seed_end, pfam_family, seed_pfname]) + "\n")
        elif line[0].isalnum():
            seed_pfname = line.split()[0]
            seed_seq = line.split()[1]
            seeds_seq_file.write(">" + pfamnaming2newnaming[seed_pfname] + "\n" + seed_seq.strip().replace(".",'').upper() + "\n")
    seed_unipids_file.write("\n".join(sorted(list(set(unipids_lst)))))
    seed_unipver_ids_file.write("\n".join(sorted(list(set(unipids_ver_lst)))))