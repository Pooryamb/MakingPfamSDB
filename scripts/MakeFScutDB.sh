set -e
mkdir -p ../FLPSS ../PfamSDB_fscut

foldseek createdb ../structures/FLPSS.tar ../FLPSS/FLPSS
foldseek compressca ../FLPSS/FLPSS ../FLPSS/FLPSS_ca_f64 --coord-store-mode 3

foldseek lndb ../FLPSS/FLPSS_h ../FLPSS/FLPSS_ss_h
foldseek lndb ../FLPSS/FLPSS_h ../FLPSS/FLPSS_ca_f64_h

foldseek convert2fasta ../FLPSS/FLPSS ../FLPSS/FLPSS.fasta
foldseek convert2fasta ../FLPSS/FLPSS_ss ../FLPSS/FLPSS_ss.fasta
foldseek convert2fasta ../FLPSS/FLPSS_ca_f64 ../FLPSS/FLPSS_ca.fasta


python PfamSDB_fscut.py


foldseek tsv2db ../PfamSDB_fscut/PfamSDB_fscut.tsv ../PfamSDB_fscut/PfamSDB_fscut --output-dbtype 0
foldseek tsv2db ../PfamSDB_fscut/PfamSDB_fscut_ss.tsv ../PfamSDB_fscut/PfamSDB_fscut_ss --output-dbtype 0
foldseek tsv2db ../PfamSDB_fscut/PfamSDB_fscut_h.tsv ../PfamSDB_fscut/PfamSDB_fscut_h --output-dbtype 12
foldseek tsv2db ../PfamSDB_fscut/PfamSDB_fscut_ca.tsv ../PfamSDB_fscut/PfamSDB_fscut_ca --output-dbtype 12
foldseek compressca ../PfamSDB_fscut/PfamSDB_fscut ../PfamSDB_fscut/PfamSDB_fscut_ca2 --coord-store-mode 2
foldseek rmdb ../PfamSDB_fscut/PfamSDB_fscut_ca
foldseek mvdb ../PfamSDB_fscut/PfamSDB_fscut_ca2 ../PfamSDB_fscut/PfamSDB_fscut_ca
