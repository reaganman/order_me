import sys
from Bio import Phylo, SeqIO

def update_descriptions(treefile, fastafile, outputfile):
    """
    Update sequence descriptions in a Newick-formatted tree file based on information from a FASTA file.

    Parameters:
        treefile (str): Path to the input Newick-formatted phylogenetic tree file.
        fastafile (str): Path to the input FASTA file containing sequences with descriptions.
        outputfile (str): Path to save the updated Newick tree file.

    Returns:
        None
    """
    # Read the phylogenetic tree from the Newick file
    tree = Phylo.read(treefile, 'newick')

    # Read sequences from the FASTA file
    sequences_dict = {}
    for record in SeqIO.parse(fastafile, "fasta"):
        seq_id = record.id
        if seq_id not in sequences_dict:
            sequences_dict[seq_id] = [record]
        else:
            sequences_dict[seq_id].append(record)


    # Update descriptions in the tree
    for leaf in tree.get_terminals():
        sequence_id = leaf.name
        if sequence_id in sequences_dict:
            description = sequences_dict[sequence_id][0].description
            leaf.name = description

    # Write the updated tree to the output file
    Phylo.write(tree, outputfile, 'newick')

if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python update_descriptions.py <treefile> <fastafile> <outputfile>")
        sys.exit(1)

    # Get the input treefile, fastafile, and outputfile from command-line arguments
    treefile = sys.argv[1]
    fastafile = sys.argv[2]
    outputfile = sys.argv[3]

    # Call the update_descriptions function with the provided arguments
    update_descriptions(treefile, fastafile, outputfile)

