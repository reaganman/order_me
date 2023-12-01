#!/bin/bash
# Script for building a phylogenetic tree using IQ-TREE and visualizing it

# Usage: bash make_tree.sh <alignment_file.fasta>

# Check if the correct number of command-line arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: bash make_tree.sh <alignment_file.fasta>"
    exit 1
fi

# Assign the input alignment file from the command-line argument
alignment="$1"

# Check if the input alignment file exists
if [ ! -f "$alignment" ]; then
    echo "Error: Input alignment file '$alignment' not found."
    exit 1
fi

# Load IQ-TREE module
module load iqtree

# Build phylogenetic tree using IQ-TREE with 1000 bootstrap replicates
iqtree2 -s "$alignment" -B 1000 -redo

# Check if IQ-TREE process was successful
if [ $? -ne 0 ]; then
    echo "Error: IQ-TREE failed to build the phylogenetic tree."
    exit 1
fi

# Define output file names for the tree plot
out_file="${alignment%.fasta}_tree.png"
contree_file="$alignment.contree"

# Check if the contree file was generated
if [ ! -f "$contree_file" ]; then
    echo "Error: IQ-TREE failed to generate the contree file."
    exit 1
fi

# Display the names of the output files
echo "Tree plot saved as: $out_file"
echo "Contree file generated: $contree_file"

# Visualize the phylogenetic tree using a Python script (view_tree.py)
python3 view_tree.py "$contree_file" "$out_file"

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to visualize the phylogenetic tree."
    exit 1
fi
