DOWNLOADER := aria2c -x16 -s32

.PHONY: all pfamsdb_fscut

all: pfamsdb.tar


./tmp/unip_ids_af.tsv:
	mkdir -p ./tmp
	gsutil -m cp "gs://public-datasets-deepmind-alphafold-v4/manifests/manifest-model_v4_cif-part-*.csv" ./tmp
	find ./tmp -name 'manifest-model_v4_cif-part-*.csv' | parallel sed -i "'s/AF-\(.*\)-F1-model_v4\.cif/\1/'" {}
	sort ./tmp/manifest-model_v4_cif-part-0* > $@
	rm ./tmp/manifest*

./tmp/Pfam-A.seed.gz:
	mkdir -p tmp/
	$(DOWNLOADER) https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.seed.gz
	mv Pfam-A.seed.gz ./tmp

./tmp/unip_ids_pf.tsv ./tmp/unipver_ids_pf.tsv ./tmp/seeds_seq.fasta: ./tmp/Pfam-A.seed.gz
	zcat ./tmp/Pfam-A.seed.gz | ./process_pfam_seeds_file.py
	
./tmp/af_pf_intersect.tsv: ./tmp/unip_ids_pf.tsv ./tmp/unip_ids_af.tsv
	comm -12 $^ > $@

./tmp/downloading_cifs_successful: ./tmp/af_pf_intersect.tsv
	awk '{print "gs://public-datasets-deepmind-alphafold-v4/AF-" $$1 "-*_v4.cif"}' ./tmp/af_pf_intersect.tsv > ./tmp/af_pf_intersect_urls.txt
	mkdir -p ./tmp/flpss
	cat ./tmp/af_pf_intersect_urls.txt | gsutil -m -q cp -I ./tmp/flpss 2> ./tmp/gsutil_cif_download_errors.log
	if [ ! -s "./tmp/gsutil_cif_download_errors.log" ]; then touch "./tmp/downloading_cifs_successful"; else echo "Errors log is not empty."; fi
	
./tmp/renaming_cifs_successful: ./tmp/downloading_cifs_successful
	find tmp/flpss -name "AF-*-F1-model_v4.cif" | parallel 'mv {} {= s:AF-(.*)-F1-model_v4.cif:\1: =}.cif'
	touch ./tmp/renaming_cifs_successful

./tmp/flpss_af.fasta: ./tmp/renaming_cifs_successful
	./extract_fasta_from_afcifs.py

./tmp/pfamseq.gz:
	mkdir -p tmp/
	$(DOWNLOADER) https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/pfamseq.gz
	mv pfamseq.gz ./tmp

./tmp/flpss_pfam.fasta: ./tmp/pfamseq.gz ./tmp/unipver_ids_pf.tsv
	seqtk subseq ./tmp/pfamseq.gz ./tmp/unipver_ids_pf.tsv > ./tmp/flpss_pfam.fasta

./tmp/seeds_coords_on_afdb.tsv: ./tmp/flpss_pfam.fasta ./tmp/flpss_af.fasta ./tmp/seeds_seq.fasta
	./map_seeds2afdb.py

./tmp/cutting_cifs_successful: ./tmp/seeds_coords_on_afdb.tsv ./tmp/downloading_cifs_successful
	mkdir -p ./tmp/pfamsdb
	./cut_flpss_cifs.py 2> ./tmp/cutting_errors.log
	if [ ! -s "./tmp/cutting_errors.log" ]; then touch "./tmp/cutting_cifs_successful"; else echo "There was an error in cutting cifs"; fi
	
flpss.tar: ./tmp/downloading_cifs_successful
	cd ./tmp/flpss && \
	find . -type f ! -name '*.gz' -exec gzip "{}" + && \
	find . -type f -name '*.gz' -print0 | tar cf ../flpss.tar --null -T - && \
	cd ../..
	mv ./tmp/flpss.tar .
	
pfamsdb.tar: ./tmp/cutting_cifs_successful
	cd ./tmp/pfamsdb && \
	find . -type f ! -name '*.gz' -exec gzip "{}" + && \
	find . -type f -name '*.gz' -print0 | tar cf ../pfamsdb.tar --null -T - && \
	cd ../..
	mv ./tmp/pfamsdb.tar .
	
./tmp/flpss_fsdb/flpss_ca.fasta: flpss.tar
	mkdir ./tmp/flpss_fsdb
	foldseek createdb flpss.tar ./tmp/flpss_fsdb/flpss_fsdb
	foldseek lndb ./tmp/flpss_fsdb/flpss_fsdb_h ./tmp/flpss_fsdb/flpss_fsdb_ss_h
	foldseek lndb ./tmp/flpss_fsdb/flpss_fsdb_h ./tmp/flpss_fsdb/flpss_fsdb_ca_f64_h
	foldseek compressca ./tmp/flpss_fsdb/flpss_fsdb ./tmp/flpss_fsdb/flpss_fsdb_ca_f64 --coord-store-mode 3
	foldseek convert2fasta ./tmp/flpss_fsdb/flpss_fsdb ./tmp/flpss_fsdb/flpss.fasta
	foldseek convert2fasta ./tmp/flpss_fsdb/flpss_fsdb_ss ./tmp/flpss_fsdb/flpss_ss.fasta
	foldseek convert2fasta ./tmp/flpss_fsdb/flpss_fsdb_ca_f64 ./tmp/flpss_fsdb/flpss_ca.fasta
	foldseek rmdb ./tmp/flpss_fsdb/flpss_fsdb_ca_f64
	foldseek rmdb ./tmp/flpss_fsdb/flpss_fsdb_ca_f64_h

./tmp/pfamsdb_fscut/pfamsdb_fscut_ca.tsv: ./tmp/flpss_fsdb/flpss_ca.fasta ./tmp/seeds_coords_on_afdb.tsv
	mkdir ./tmp/pfamsdb_fscut
	./cut_fasta.py
	
pfamsdb_fscut: ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca.tsv
	foldseek tsv2db ./tmp/pfamsdb_fscut/pfamsdb_fscut.tsv ./tmp/pfamsdb_fscut/pfamsdb_fscut --output-dbtype 0
	foldseek tsv2db ./tmp/pfamsdb_fscut/pfamsdb_fscut_ss.tsv ./tmp/pfamsdb_fscut/pfamsdb_fscut_ss --output-dbtype 0
	foldseek tsv2db ./tmp/pfamsdb_fscut/pfamsdb_fscut_h.tsv ./tmp/pfamsdb_fscut/pfamsdb_fscut_h --output-dbtype 12
	foldseek tsv2db ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca.tsv ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca --output-dbtype 12
	foldseek compressca ./tmp/pfamsdb_fscut/pfamsdb_fscut ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca2 --coord-store-mode 2
	foldseek rmdb ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca
	foldseek mvdb ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca2 ./tmp/pfamsdb_fscut/pfamsdb_fscut_ca
	mv ./tmp/pfamsdb_fscut .
	
clean:
	find ./tmp/ -type f | parallel rm
	rm -r ./tmp/
