#!/bin/bash

# First, It will get the names of the files from the following page address:
# https://console.cloud.google.com/storage/browser/public-datasets-deepmind-alphafold-v4/manifests


set -e

echo "Starting to download manifest files from AlphafoldDB"

TMPpath=$1
gsutil -m cp \
  "gs://public-datasets-deepmind-alphafold-v4/manifests/manifest-model_v4_cif-part-*.csv" \
  $TMPpath


echo "Converting the Manifest files to Uniprot IDs"
python ConvertManifest2UnipID.py 


echo "Removing Manifest files"
rm ${TMPpath}/manifest-model*.csv

echo "Marging file names to have a single file containing all IDs"
python MergeFileNames.py


echo "Removing temp files"
rm $TMPpath/part-*.csv $TMPpath/merged_*