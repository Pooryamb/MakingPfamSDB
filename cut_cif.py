import re

def cut_cif(fhandle, cut_start, cut_end):
    """
    Convert a structure in mmCIF format to PDB format, and cuts the structure
    ------
    This function has been created by adjusting the code available in 
    https://f1000research.com/articles/7-1961
    """

    in_section, read_atom = False, False
    label_pos = 0
    labels = {}
    cif_header = ["data_B1\n", "#\n"]
    cif_pos_header = ["loop_\n"]
    model_data = []  
    for line in fhandle:
        if line.startswith('loop_'):  # start of section
            in_section = True

        elif line.startswith('#'):  # end of section
            in_section = False
            read_atom = False

        elif in_section and line.startswith('_atom_site.'):  # ATOM/HETATM
            read_atom = True
            labels[line.strip()] = label_pos
            label_pos += 1
            cif_pos_header.append(line)

        elif read_atom and line.startswith(('ATOM', 'HETATM')):  # convert
            fields = re.findall(r'[^"\s]\S*|".+?"', line)  # find enclosed ''

            fid = labels.get('_atom_site.label_seq_id')
            resnum = int(fields[fid])
       
            if resnum > cut_end:
                break

            if resnum >= cut_start:
                model_data.append(line)

    model_data.append("#\n")
    cut_cif_lines = cif_header + cif_pos_header + model_data
    return "".join(cut_cif_lines)
