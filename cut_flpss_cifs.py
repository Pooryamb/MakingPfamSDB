#!/usr/bin/env python3
import os
import glob
from concurrent.futures import ProcessPoolExecutor
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from cut_cif import cut_cif

def cut_flpss_on_domain_borders(cut_data):
    cif_content = open(f"./tmp/flpss/{cut_data[0]}.cif").readlines()
    chopped_cif = cut_cif(cif_content, cut_data[1], cut_data[2])
    cut_id = "_".join(map(str, cut_data))
    with open(f"./tmp/pfamsdb/{cut_id}.cif", 'w') as cut_file:
        cut_file.write("".join(chopped_cif))

files = os.listdir("./tmp/flpss/")
unip_ids = [x.replace(".cif", '') for x in files]
    
seed_coords = pd.read_csv("./tmp/seeds_coords_on_afdb.tsv", sep="\t", header=None)
seed_coords_aslist = seed_coords.values.tolist()
    
with ProcessPoolExecutor() as executor:
    # Map the cut_flpss_on_domain_borders function to each item in seed_coords_aslist
    executor.map(cut_flpss_on_domain_borders, seed_coords_aslist)