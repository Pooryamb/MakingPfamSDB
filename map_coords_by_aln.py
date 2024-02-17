from Bio.Align import PairwiseAligner
from Bio.Align import substitution_matrices

aligner = PairwiseAligner()
aligner.mode = 'global'
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.open_gap_score = -10
aligner.extend_gap_score = -0.5
aligner.target_end_gap_score = 0.0
aligner.query_end_gap_score = 0.0

def process_aln_ouput_from_pairwisealigner(line):
    if len(line.split()) <3:
        return ""
    return line.split()[2]

def get_aln_match_seq(line):
    if len(line.split())>=2:
        return line.split()[1]
    return ""

def get_raw_aln(seq1,seq2):
    alignments = aligner.align(seq1,seq2)
    alnfmt = alignments[0].format().split("\n")
    seq1aln = "".join([process_aln_ouput_from_pairwisealigner(x) for x in alnfmt[0::4]]) #if len(x.split())==4
    seq2aln = "".join([process_aln_ouput_from_pairwisealigner(x) for x in alnfmt[2::4]])
    alnmatching = "".join([get_aln_match_seq(x) for x in alnfmt[1::4]])
    return seq1aln, seq2aln, alnmatching

def map_coords_by_aln(seq1, seq2, seq1start, seq1end):
    aln1,aln2,alnmatching = get_raw_aln(seq1,seq2)
    
    aln1cursor, aln2cursor,seq2start,seq2end = 0,0,0,0
    aln_start, aln_end = 0,0
    for i in range(len(aln1)):
        if aln1[i] != "-": aln1cursor += 1
        if aln2[i] != "-": aln2cursor += 1
        if aln1cursor == seq1start: 
            seq2start=aln2cursor
            aln_start = i
        elif aln1cursor == seq1end: 
            seq2end=aln2cursor
            aln_end=i
            break;
    if (seq2start==0) or (seq2end==0):
        return -1, -1,-1
    dom1len = seq1end - seq1start +1
    dom2len = seq2end - seq2start +1
    fident = alnmatching[aln_start:aln_end+1].count("|")/(min(dom1len,dom2len))
    
    return seq2start, seq2end, fident
