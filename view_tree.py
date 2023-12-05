import sys
from Bio import Phylo
import matplotlib.pyplot as plt

def view_tree(treefile, outfile):
    """
    Read and visualize a phylogenetic tree from a Newick-formatted file.

    Parameters:
        treefile (str): Path to the Newick-formatted phylogenetic tree file.
        outfile (str): Path to save the output image file.

    Returns:
        None
    """
    # Read the phylogenetic tree from the Newick file
    tree = Phylo.read(treefile, 'newick')

    # Create a larger figure size (adjust the width and height as needed)
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw and display the phylogenetic tree
    Phylo.draw(tree, axes=ax)

    # Show the plot
    plt.show()

    # Save the plot to the specified output file
    plt.savefig(outfile)

if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python view_tree.py <treefile> <outfile>")
        sys.exit(1)

    # Get the treefile and outfile from command-line arguments
    treefile = sys.argv[1]
    outfile = sys.argv[2]

    # Call the view_tree function with the provided arguments
    view_tree(treefile, outfile)
