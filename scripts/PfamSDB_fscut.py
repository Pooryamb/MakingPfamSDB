#!/usr/bin/env python3

#This script has been adopted from the github of Dr. Milot Mirdita: https://github.com/milot-mirdita/MakingPfamSDB/tree/cut-fs-db

def remove_extension(header):
    return header.split(".")[0]

def return_fasta_dict(file_path, header_transform):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
    seq_dict = {header_transform(lines[i].strip(">")): lines[i + 1].upper() for i in range(0, len(lines), 2)}
    return seq_dict

def return_coordinates_dict(file_path, header_transform):
    with open(file_path, 'r') as file:
        lines = file.read().strip().split("\n")
    coords_dict = {}
    for i in range(0, len(lines), 2):
        header = header_transform(lines[i].strip(">"))
        csv_data = lines[i + 1].strip()
        coords = [float(val) for val in csv_data.split(',')]
        
        # Ensure the number of coordinates is a multiple of 3
        if len(coords) % 3 != 0:
            print(f"Error: number of coordinates for header {header} is not a multiple of 3")
            continue

        coords_dict[header] = coords
    return coords_dict

tmp_dir = "./tmp"
flpss_dir = "../FLPSS"

pfam_seeds_fl_af = return_fasta_dict(f"{flpss_dir}/FLPSS.fasta", remove_extension)
pfam_seeds_fl_af_ss = return_fasta_dict(f"{flpss_dir}/FLPSS_ss.fasta", remove_extension)
pfam_coords = return_coordinates_dict(f"{flpss_dir}/FLPSS_ca.fasta", remove_extension)

retained_seqs_af = {}
retained_seqs_af_ss = {}
retained_coords = {}

with open(f"{tmp_dir}/PfamCordsOnSeedsOneLineFormatAFadj.tsv", 'r') as pfam_cords:
    for line in pfam_cords:
        try:
            seq_id, cords_and_pfs = line.strip("\n").split("\t")
            if len(cords_and_pfs.strip())==0:
                continue
        except ValueError:
            print(line)
            raise
        
        if seq_id not in pfam_seeds_fl_af or seq_id not in pfam_seeds_fl_af_ss or seq_id not in pfam_coords:
            continue

        cords_and_pfs = cords_and_pfs.split(",")
        if len(cords_and_pfs)==0: 
            continue
        for i in range(0, len(cords_and_pfs), 3):
            try:
                start, end, _ = int(cords_and_pfs[i]), int(cords_and_pfs[i + 1]), cords_and_pfs[i + 2]
                key = f"{seq_id}_{start}_{end}_{_}"
                retained_seqs_af[key] = pfam_seeds_fl_af[seq_id][start-1:end]
                retained_seqs_af_ss[key] = pfam_seeds_fl_af_ss[seq_id][start-1:end]
            
                # Adjust slicing for x,y,z format in base64 encoded binary floats
                total_len = len(pfam_coords[seq_id]) // 3
                x_slice = pfam_coords[seq_id][(start-1):end]
                y_slice = pfam_coords[seq_id][total_len + (start-1):total_len + end]
                z_slice = pfam_coords[seq_id][2*total_len + (start-1):2*total_len + end]
                retained_coords[key] = x_slice + y_slice + z_slice
            except:
                print("There is an error while processing this line\n" + line)

fscut_dir = "../PfamSDB_fscut"
with open(f"{fscut_dir}/PfamSDB_fscut.tsv", 'w') as outfile1, \
     open(f"{fscut_dir}/PfamSDB_fscut_ss.tsv", 'w') as outfile2, \
     open(f"{fscut_dir}/PfamSDB_fscut_h.tsv", 'w') as outfile3, \
     open(f"{fscut_dir}/PfamSDB_fscut_ca.tsv", 'w') as outfile4:
    i = 0
    for seq_id, seq in retained_seqs_af.items():
        outfile1.write(f"{i}\t{seq}\n")
        outfile2.write(f"{i}\t{retained_seqs_af_ss[seq_id]}\n")
        outfile3.write(f"{i}\t{seq_id}\n")
        coords_str = ",".join(map(str, retained_coords[seq_id]))
        outfile4.write(f"{i}\t{coords_str}\n")
        i += 1

