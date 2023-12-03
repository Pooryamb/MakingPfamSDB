import sys
tmp = sys.argv[1]
file1add = f"{tmp}/AllAF_IDs.csv"
file2add = f"{tmp}/JustIDsOfSeeds.csv"
outputadd = f"{tmp}/SeedAFIntersection.tsv"

with open(file1add, "r") as file1, open(file2add, "r") as file2, open(outputadd, "w") as merged_file:
    line1 = file1.readline()
    line2 = file2.readline()

    while line1 and line2:
        if line1 < line2:
            line1 = file1.readline()
        elif line1 > line2:
            line2 = file2.readline()
        elif line1.strip()==line2.strip():
            merged_file.write(line1.strip() + "\n")
            line2 = file2.readline()
            line1 = file1.readline()

    while line1:
        line1 = file1.readline()

    while line2:
        line2 = file2.readline()
