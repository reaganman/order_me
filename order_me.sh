#!/bin/bash
#
# order_me.sh - Main script for the order_me package, a pipeline using search and alignment algorithms to identify sequences homologous to a user specified sequences, in a users specified taxonomic order. Functionality for makeing a gene tree is included.
#
# Usage: bash order_me.sh --query <query> --taxid <taxid> --email <email> [other options...]
#

# Load environment
#conda env create -f order_me_env.yml
#conda activate order_me_environment

# Set default values
query=''
taxid=''
email=''

module load blast
module load mafft
module load iqtree

# Set default values
save_path=$(pwd)
evalue=0.0001
blast_type=blastn_short

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
        --query)
            query="$2"
            shift
            shift
            ;;
        --taxid)
            taxid="$2"
            shift
            shift
            ;;
        --save_path)
            save_path="$2"
            shift
            shift
            ;;
        --evalue)
            evalue="$2"
            shift
            shift
            ;;
        --email)
            email="$2"
            shift
            shift
            ;;
        --blast_type)
            blast_type="$2"
            shift
            shift
            ;;
        --setup)
            setup="$2"
            shift
            shift
            ;;
        *)
            echo "UNKNOWN OPTION: $1"
            echo "USAGE: bash order_me.sh --query <query> --taxid <taxid> --email <email> [other options...]"
            exit 1
            ;;
    esac
done

# Check if required options are provided
if [[ ! "$query" || ! "$taxid" || ! "$email" ]]; then 
    echo "USAGE: bash order_me.sh --query <query> --taxid <taxid> --email <email> [other options...]"
    exit 1
fi

# Set up a log file
log="$query"_in_"$taxid"_log.txt

# Download and translate the query
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=$query&rettype=fasta&retmode=text" > "$query".fasta
python3 get_translation.py "$query".fasta "$query".fa

# Perform setup if specified
if [[ "$setup" ]]; then
    echo "Downloading assemblies and making BLAST databases!"
    bash setup_blast.sh --save_path "$save_path" --taxid "$taxid" --email "$email"
fi

# Run BLAST and merge results
Assemblies="$save_path"/Assemblies_"$taxid"/
final_aligned_results="$query"_in_"$taxid"_"$blast_type".fasta
bash blast_em.sh --Assemblies "$Assemblies" --query "$query" --blast_type "$blast_type" --evalue "$evalue" --output_alignment "$final_aligned_results"

echo "Alignment created: $query/$final_aligned_results"
echo "Check alignment then generate a consensus tree with: bash make_tree.sh $query/$final_aligned_results"

# Create a results directory if it doesn't exist
results_dir="$query"
if [[ ! -d "$results_dir" ]]; then 
    mkdir "$results_dir"
fi
mv *"$query"* "$results_dir" 

