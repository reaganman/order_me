query=$1 #accesion number for gene/sequence to blast
taxid=$2 #8342 taxid associated with order, find on https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/ 
path_to_genomes=$3 #/scratch/general/nfs1/utu_4310/fr10_evolution_wd/test_get_genomes
evalue=$4
email=$5
blast_type=$6
Genomes="$path_to_genomes"/Genomes_"$taxid"/*

module load blast
module load mafft
module load iqtree

#download query
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=$query&rettype=fasta&retmode=text" > "$query".fasta

python3 get_translation.py "$query".fasta "$query".fa  #translate query

#download genomes
#python3 get_genomes.py --taxid $taxid --email $email --save_path $path_to_genomes

#unzip the fnas
#for genome in $Genomes; do
#	gunzip "$genome"/*fna.gz;
#done

#make blast dbs
#for genome in $Genomes; do
#    for fna_file in $(find "$genome" -name '*.fna'); do
#        makeblastdb -dbtype nucl -in "$fna_file" -out "${fna_file%.fna}.db"
#    done
#done

#run blast and merge results
merged_results="$query"_in_"$taxid".fasta
bash blast_em.sh "$Genomes" "$query" "$blast_type" "$evalue" "$merged_results"


#generate tree

bash make_tree.sh "$merge_results"


