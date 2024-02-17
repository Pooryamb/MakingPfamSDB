#!/usr/bin/env python3
from fasta2dict import fasta2dict, identity_header, extract_prefix
from map_coords_by_aln import map_coords_by_aln

seeds_fasta_path = "./tmp/seeds_seq.fasta"
af_flpss_path = "./tmp/flpss_af.fasta"
pfam_flpss_path = "./tmp/flpss_pfam.fasta"
seeds_on_afdb_path = "./tmp/seeds_coords_on_afdb.tsv"

with open(seeds_on_afdb_path, 'w') as seeds_on_afdb_file:
    seeds_seq_dict = fasta2dict(seeds_fasta_path, identity_header)
    af_flpss_dict = fasta2dict(af_flpss_path, identity_header)
    pfam_flpss_dict = fasta2dict(pfam_flpss_path, extract_prefix)
    
    for seed_id in seeds_seq_dict.keys():
        unipid, domstart, domend, pfid = seed_id.split("_")
        domstart, domend = int(domstart), int(domend)
        if unipid not in af_flpss_dict.keys():
            continue
        if af_flpss_dict[unipid][domstart-1:domend] == seeds_seq_dict[seed_id]:
            seeds_on_afdb_file.write(f"{unipid}\t{domstart}\t{domend}\t{pfid}\n")
        else:
            if unipid not in pfam_flpss_dict.keys():
                continue
            domstart_af, domend_af, fident = map_coords_by_aln(pfam_flpss_dict[unipid], af_flpss_dict[unipid],domstart, domend )
            if fident == 1:
                seeds_on_afdb_file.write(f"{unipid}\t{domstart_af}\t{domend_af}\t{pfid}\n")