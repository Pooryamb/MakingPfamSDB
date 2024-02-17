#!/usr/bin/env python3
# With special thanks to Dr. Milot Mirdita for providing the instructions on cutting a Foldseek database
def cut_normalseq(seq, domstart, domend):
    return seq[domstart-1:domend]
    
def cut_caseq(seq, domstart, domend):
    pdb_coords = seq.strip().split(",")
    res_count = len(pdb_coords)//3
    x_coords = pdb_coords[domstart - 1: domend]
    y_coords = pdb_coords[res_count + domstart-1: res_count + domend]
    z_coords = pdb_coords[2*res_count + domstart-1: 2*res_count + domend]
    all_coords = x_coords + y_coords + z_coords
    return ",".join(map(str, all_coords))

cut_coords = {}
with open("./tmp/seeds_coords_on_afdb.tsv") as seed_coords:
    for line in seed_coords:
        unipid, domstart, domend, pfid = line.strip().split("\t")
        domstart, domend = int(domstart), int(domend)
        cut_positions = cut_coords.get(unipid, [])
        cut_positions.append([domstart, domend, pfid])
        cut_coords[unipid] = cut_positions
        
non_unipids= []
i=0
with open("./tmp/flpss_fsdb/flpss.fasta") as seq_file, \
     open("./tmp/flpss_fsdb/flpss_ss.fasta") as ss_seq_file, \
     open("./tmp/flpss_fsdb/flpss_ca.fasta") as ca_seq_file, \
     open("./tmp/pfamsdb_fscut/pfamsdb_fscut.tsv", 'w') as cut_seq_file, \
     open("./tmp/pfamsdb_fscut/pfamsdb_fscut_ss.tsv", 'w') as cut_ss_seq_file, \
     open("./tmp/pfamsdb_fscut/pfamsdb_fscut_ca.tsv", 'w') as cut_ca_seq_file, \
     open("./tmp/pfamsdb_fscut/pfamsdb_fscut_h.tsv", 'w') as cut_h_file:
    while True:
        unipid = seq_file.readline().strip().replace(".cif.gz", '').lstrip(">")
        fl_seq = seq_file.readline().strip()
        if len(unipid) == 0 :
            break
        _, __ = ss_seq_file.readline(),  ca_seq_file.readline()
        fl_ss_seq, fl_ca_seq = ss_seq_file.readline().strip(),  ca_seq_file.readline().strip()
        
        if unipid not in cut_coords:
            non_unipids.append(unipid)
            continue
            
        for cut_positions in cut_coords[unipid]:
            domstart, domend, pfid = cut_positions
            cut_seq_id = f"{unipid}_{domstart}_{domend}_{pfid}"
            cut_seq = cut_normalseq(fl_seq, domstart, domend)
            cut_ss_seq= cut_normalseq(fl_ss_seq, domstart, domend)
            cut_ca_seq=cut_caseq(fl_ca_seq, domstart, domend)
            
            cut_h_file.write(f"{i}\t{cut_seq_id}\n")
            cut_ca_seq_file.write(f"{i}\t{cut_ca_seq}\n")
            cut_ss_seq_file.write(f"{i}\t{cut_ss_seq}\n")
            cut_seq_file.write(f"{i}\t{cut_seq}\n")
            i+=1