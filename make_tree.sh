alignment=$1
module load iqtree

iqtree2 -s "$alignment" -B 1000 -redo
out_file="${alignment%.fasta}_tree.png"
echo "$out_file"
echo "$alignment".treefile
python3 view_tree.py "$alignment".treefile "$out_file"
