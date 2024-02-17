# Making the Structural Database for Pfam (PfamSDB)

This GitHub repository is dedicated to creating the Pfam seeds structure database (PfamSDB)
by cutting the related full-length structures at their domain borders. 
 

## Requirements

### Software Dependencies
- aria2c==1.36.0
- Python==3.10.12
- gsutil==5.7 (Access to the AlphaFold database is assumed)
- GNU parallel==20210822
- seqtk==1.4
- Foldseek==8-ef4e960

Python package dependencies are provided inside the `requirements.txt` file.

### Hardware Requirements
- High-speed internet connection
- At least 700GB of storage, preferably on a high-speed SSD

### Installation
Ensure you have the required software installed. Python libraries can be installed via the `requirements.txt` file

## Usage

To create the database of cif files for Pfam seeds, use the `make` command.

For users who prefer to query protein structures against the PfamSDB using 
Foldseek, there is an alternative approach to constructing PfamSDB. 
Instead of utilizing cif files of the structures, this method involves 
segmenting the Foldseek database along the domain borders. 
This alternative technique can be executed using the `make pfamsdb_fscut` command


To clean up and remove any intermediate files generated during the construction of 
PfamSDB, you can use the `make clean` command:

## Cite Us

If you use PfamSDB or any associated tools in your research, please consider citing our work. Here's the citation format:

Borujeni PM, Salavati R. Functional domain annotation by structural similarity. NAR Genomics and Bioinformatics. 2024 Mar 1;6(1).

BibTeX entry for LaTeX users:

@article{borujeni2024functional,
  title={Functional domain annotation by structural similarity},
  author={Borujeni, Poorya Mirzavand and Salavati, Reza},
  journal={NAR Genomics and Bioinformatics},
  volume={6},
  number={1},
  pages={lqae005},
  year={2024},
  publisher={Oxford University Press}
}