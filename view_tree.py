import sys
from Bio import Phylo
import matplotlib.pyplot as plt

def view_tree(treefile, outfile):
    tree = Phylo.read(treefile, 'newick')
    Phylo.draw(tree)
    plt.show
    plt.savefig(outfile)

if __name__ == '__main__':
    treefile = sys.argv[1]
    outfile = sys.argv[2]
    view_tree(treefile, outfile)

