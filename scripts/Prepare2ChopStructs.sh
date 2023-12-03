set -e
TMP="./tmp"
wget -P $TMP https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/pfamseq.gz
seqtk subseq $TMP/pfamseq.gz $TMP/pfamseqid.csv > $TMP/FLPSS_PS.fasta
cat $TMP/B*.fasta > $TMP/FLPSS_AF.fasta
rm $TMP/B*.fasta
python FindDiffBetAFdbAndPfamSeqAndAdjustCordsFile.py $TMP
NumOfJobs=$(find ../structures/ -maxdepth 1 -regextype posix-extended -regex '../structures/B[0-9]+\.tar' | wc -l)
python SplitPfamCordsFiles.py $NumOfJobs
