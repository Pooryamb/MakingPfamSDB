def identity_header(seq_header):
    return seq_header

def extract_prefix(seq_header):
    return seq_header.split(".")[0]
    
def fasta2dict(filepath, header_processor):
    seq_dict = {}
    with open(filepath) as file:
        lines = file.readlines()
        seq_dict = {header_processor(lines[i].strip().strip(">")): lines[i +1].strip().upper() for i in range(0, len(lines), 2)}
        
    return seq_dict