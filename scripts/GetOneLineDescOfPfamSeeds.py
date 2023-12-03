import pandas as pd
import sys


tmp = sys.argv[1]

PfCords = pd.read_csv(f"{tmp}/PfamSeedsTwoIDsAndLocs.tsv", sep="\t", header=None)
PfamSeedsInAF = open(f"{tmp}/SeedAFIntersection.tsv").readlines()
PfamSeedsInAF = [x.strip() for x in PfamSeedsInAF]

PfCords = PfCords[PfCords[0].isin(PfamSeedsInAF)]

PfCords.sort_values(by=0, inplace=True)
PfCords = PfCords[[0,1,2,3]]
PfCords.reset_index(drop=True, inplace=True)
PfCords[3] = PfCords[1].astype(str) + ","+ PfCords[2].astype(str) + ","+ PfCords[3]

PfCords = PfCords[[0,3]]

PfCordsConcat = PfCords.groupby(0).agg({3:lambda x: ','.join(x)}).reset_index()
PfCordsConcat.to_csv(f"{tmp}/PfamCordsOnSeedsOneLineFormat.tsv", sep="\t", index=None, header=None)
