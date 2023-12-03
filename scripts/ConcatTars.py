import os
from math import ceil

def ConcatTars(files, outputFileName):

    level = 0
    while len(files)!= 1:
        NumOfBatches = ceil(len(files)/2)
        NewNames = []
        for i in range(NumOfBatches):
            files2merge = files[2*i:2*i+2]
            outfileName = f"./tmp/merged_tar_level_{level}_num_{i}.tar"
            os.system(f"cp {files2merge[0]} {outfileName}")
            if len(files2merge)==2:
                os.system(f"tar -Af {outfileName} {files2merge[1]}")

            NewNames.append(outfileName)
        files = NewNames
        level += 1
    os.system(f"mv {files[0]} {outputFileName}")
    os.system("rm tmp/merged_tar_*.tar")
