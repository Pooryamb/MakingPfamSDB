# To run this script, you must have extracted the amino acid sequence of the Pfam
# Seeds, and then chop the regions where Pfam were predicted.
from MapSeedLocsOnAF import map_coords_by_aln
import re
import sys
tmp = sys.argv[1]
fident_threshold_for_domain = 1
pfam_flpss_processor = lambda header: header.strip().lstrip(">").split(".")[0]
remove_first_char = lambda x:x[1:]

def ReturnFastaDict(fileAdd, header_processor):
    file = open(fileAdd)
    lines = file.read().strip().split("\n")
    SeqDict = {}
    for i in range(0,len(lines),2):
        SeqDict[header_processor(lines[i])] = lines[i +1].upper()
    return SeqDict

def returnseqid(seqid, start, end, pf):
    return f"{seqid}_{start}_{end}_{pf}"

def make_coords_data_numeric(CordsAndPFs):
    NumCords = CordsAndPFs[:]
    for i in range(0, len(CordsAndPFs),3):
        NumCords[i] = int(NumCords[i])
        NumCords[i+1] = int(NumCords[i+1])
    return NumCords

pfamseeds = ReturnFastaDict(f"{tmp}/PfamSeeds.fasta", remove_first_char)
FLPSS_PS = ReturnFastaDict(f"{tmp}/FLPSS_PS.fasta", pfam_flpss_processor)#PS is for PfamSeq
FLPSS_AF = ReturnFastaDict(f"{tmp}/FLPSS_AF.fasta", remove_first_char)


PfamCords = open(f"{tmp}/PfamCordsOnSeedsOneLineFormat.tsv")
SeedLocationsOnAF = {}
missing_domains = 0
corrected_by_nw = 0

for line in PfamCords:
    SeqID = line.split("\t")[0]
    CordsAndPFs = make_coords_data_numeric(line.strip().split("\t")[1].split(","))
    coords = []

    for i in range(0,len(CordsAndPFs),3):
        start,end,PF = CordsAndPFs[i], CordsAndPFs[i + 1], CordsAndPFs[i + 2]
        seed_id = returnseqid(SeqID, start, end, PF)

        if FLPSS_AF[SeqID][start-1:end]==pfamseeds[seed_id]:
            coords = coords + [start, end, PF]
        else:
            missing_domains +=1
            if SeqID not in FLPSS_PS.keys():
                start_af, end_af =-1,-1
            else:
                start_af, end_af, fident = map_coords_by_aln(FLPSS_PS[SeqID],FLPSS_AF[SeqID], start, end)
            if start_af!=-1 and fident>=fident_threshold_for_domain:
                coords = coords + [start_af, end_af, PF]
                corrected_by_nw+=1
    SeedLocationsOnAF[SeqID] = coords

PfamCords.close()

print(f"{missing_domains} domain sequences could not be used based on Pfam coordinates\n {corrected_by_nw} could be used after Needleman-Wunch alignment")

PfamCorrectedCords = open(f"{tmp}/PfamCordsOnSeedsOneLineFormatAFadj.tsv",'w')
for SeqID in SeedLocationsOnAF:
    domcoordinfo = ",".join([str(x) for x in SeedLocationsOnAF[SeqID]])
    PfamCorrectedCords.write(SeqID + "\t" + domcoordinfo + "\n")

PfamCorrectedCords.close()
