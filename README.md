# order_me Pipeline
## Contents

- [Introduction](#introduction)
- [Dependencies](#dependencies)

## Introduction

`order_me` is a pipeline designed to track the evolution of a specific sequence of interest within a specified taxonomic group. It utilizes various scripts to download genomic data, perform sequence searches, and generate alignments for further analysis. Functionality to make and view phylogentics trees is also included

## Dependencies

Ensure you have the following dependencies installed before running the pipeline:

- Python 3
- BioPython
- Pandas
- blast
- iqtree
- mafft

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
Go to https://www.ncbi.nlm.nih.gov/nuccore and to find the accession ID for your sequence
[Local Image](find_queryID.png)

### 3. Get taxid for taxonomic group to search
Go to https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi and find the taxid associated with the group you want to search in

NOTE! BE CAREFUL SELECTING TAXID AS THE PIPELINE WILL DOWNLOAD ALL AVALIABLE ASSEMBLIES ASSOCIATED WITH THAT TAXID AND WHICH CAN EASILY BE > 1TB

## 4. Run pipeline with default options

$$$Going through your files I would like to see more doc strings. I think it would be helpful for them to describe the types of files that are being inputted and outputted. Also a brief overview of what the files do. The comments are helpful and I would keep those, but have a broad description in the doc string. Also, here in the readme I think it would be helpful to have a schematic that shows the progression of the files or maybe a short paragraph that describes something along the lines of "you start with file A then pass it through codeA and get file B, then yuo take file B and... etc". --Erin $$$
