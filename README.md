# order_me Pipeline
## Contents

- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [How to use](#how_to_use)
- [Run with test data](#Run_with_test_data)

## Introduction

`order_me` is a pipeline designed to track the evolution of a specific sequence of interest within a specified taxonomic group. It utilizes various scripts to download genomic data, perform sequence searches, and generate alignments for further analysis. Functionality to make and view phylogentics trees is also included

## Dependencies

Ensure you have the following dependencies available before running the pipeline:
- blast (performing local alignment search)
- Python 3 (processing blast results)
- BioPython (downloading genomes and dealing with fastas)
- Pandas (dealing with tsv blast results)
- iqtree (generating trees)
- mafft (aligning blast results)

Alternativley there is a conda environment with the required dependencies that can be loaded by running:

```bash
conda env create -f order_me_env.yml
conda activate order_me_environment
```

## How to Use

### 1. Clone the repository

```bash
git clone [repository_url]
cd order_me
```
### 2. Get accession ID for sequence of interest
Go to https://www.ncbi.nlm.nih.gov/nuccore to find the accession ID for your sequence
![Local Image](find_queryID.png)
### 3. Get taxid for taxonomic group to search
Go to https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi to find the taxid associated with the group you want to search
![Local Image](find_taxid.png)


NOTE! BE CAREFUL SELECTING TAXID AS THIS PIPELINE WILL DOWNLOAD ALL AVALIABLE ASSEMBLIES ASSOCIATED WITH THAT TAXID WHICH CAN EASILY BE > 1TB

### 4. Download assemblies and make blast dbs
```bash
bash setup_blast.sh --save_path [path] --taxid [taxonomic_id] --email [your_email]
```
--save_path is the directory where a subdirectory with the assemblies and blast dbs will be created. It's a good idea to make sure the is suffient disk space available.
Alternativley, this can be accomplished by using the --setup True option with order_me.sh
### 5. Run pipeline
```bash
bash order_me.sh --query [sequence_id] --taxid [taxonomic_id] --email [your_email] [other_options...]
```
Default options assume that assemblies direcetory is in the current directory to change this use:
```bash
--save_path [path_to_assemblies]
```
Additionally, if this is the first time searching a certain taxid, make sure to use the option:
```bash
--setup True
```
Defaults and are set to result in the maximum number of hits (blast_type = blastn_short, evalue = 0.0001) To modify this, simply use the options: 
```bash
--blast_type [blastn, blastn_short, tblastx] --evalue[your_evalue]
```
NOTE: WHILE FUNCTIONALITY FOR TBLASTX IS INCLUDED IT HAS NOT BE SUFFICENTLY TESTED AND SHOULD BE USED WITH CAUTION

Successful execution of order_me.sh will generate an alignment named:
```bash
"$query"_in_"$taxid"_"$blast_type".fasta
```

### 6. Check alignment for unmerged sequences and generate trees
When you are satisfied with the alignment generate the trees using:
```bash
bash make_tree.sh [generated_alignment]
```
## Run with test data
Test data is included with the order_me repository 
To run the pipline with this data use:
```bash
bash order_me.sh --query OR734632 --taxid 1980413 --email [your_email]
``` 
This searches the taxonomic group Hantaviridae for sequences homologous to Orthohantavirus nucleocapsid protein gene
Generated tree is included
[Local Image]( 

$$$Going through your files I would like to see more doc strings. I think it would be helpful for them to describe the types of files that are being inputted and outputted. Also a brief overview of what the files do. The comments are helpful and I would keep those, but have a broad description in the doc string. Also, here in the readme I think it would be helpful to have a schematic that shows the progression of the files or maybe a short paragraph that describes something along the lines of "you start with file A then pass it through codeA and get file B, then yuo take file B and... etc". --Erin $$$
