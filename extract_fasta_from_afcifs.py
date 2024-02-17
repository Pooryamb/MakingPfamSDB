#!/usr/bin/env python3
import re
import os
import glob
from concurrent.futures import ProcessPoolExecutor

def extract_seq(afcif_content):
    pattern = re.compile(r'_entity_poly\.pdbx_seq_one_letter_code(.*?)_entity_poly\.pdbx_seq_one_letter_code_can', re.DOTALL)
    match = pattern.search(afcif_content)
    sequence = match.group(1)
    sequence = "".join(sequence.split()).strip(";")
    return sequence

def convert_cif2fasta(cif_path):
    seq_header = os.path.basename(cif_path).replace(".cif", '')
    with open(cif_path) as cif_handle:
        cif_content = cif_handle.read()
        seq = extract_seq(cif_content)
        return f">{seq_header}\n{seq}\n"
    
flpss_cif_paths = sorted(glob.glob("./tmp/flpss/*.cif"))

with ProcessPoolExecutor() as executor:
    # map returns results as soon as they are ready, order is not guaranteed
    results = list(executor.map(convert_cif2fasta, flpss_cif_paths))

with open("./tmp/flpss_af.fasta",'w') as flpss_af_file:
    flpss_af_file.write("".join(results))
