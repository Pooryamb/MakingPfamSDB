import os
import glob
import sys
from math import ceil

tmp="./tmp"
from ConcatTars import ConcatTars

FileNum = len(glob.glob("../structures/B*_chopped.tar"))
files = [f"../structures/B{i}_chopped.tar" for i in range(1,FileNum+1)]
outputName = "../structures/PfamSDB.tar"

ConcatTars(files, outputName)

files = [f"../structures/B{i}.tar" for i in range(1,FileNum+1)]
outputName = "../structures/FLPSS.tar"
ConcatTars(files, outputName)



