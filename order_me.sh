query=$1 #accesion number for gene/sequence to blast
taxid=$2 #8342 taxid associated with order, find on https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/ 
path_to_genomes=$3 #/scratch/general/nfs1/utu_4310/fr10_evolution_wd/test_get_genomes
evalue=$4
Genomes="$path_to_genomes"/Genomes_"$taxid"/*
email=$5

echo "$query"
echo "$taxid"
echo "$path_to_genomes"
echo "$Genomes"

module load blast
module load mafft

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

#run blast
for genome in $Genomes; do  #look in each genome
    for fna_file in $(find "$genome" -name '*.fna'); do #find all blastdbs
	db_path="${fna_file%.fna}.db"
	dir_name=$(basename "$genome")
	echo "running blast with ${db_path}"
	blastn -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_blastn_results.tsv;
    blastn -task "blastn-short" -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_blastn_short_results.tsv;
    tblastx -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_tblastx_results.tsv;
    done;
done

#combine blast results
blastn_combined="aligned_blastn_results.fasta"
blastn_short_combined="aligned_blastn_short_results.fasta"
tblastx_combined="aligned_tblastx_results.fasta"
rm -f "$blastn_combined"  # Remove the combined file if they already exists
rm -f "$blastn_short_combined"
rm -f "$tblastx_combined"
results_header="stitle\tevalue\tpident\tsstart\tsend\tqseqid\tqstart\tqend\tqseq\tsseq"

for genome in $Genomes; do
    genome_name=$(basename "$genome")
    rm -f "$genome"/*combined*
    rm -f "$genome"/*fasta*
    echo "processing blast results for ${genome}"	
    for result in $(find "$genome" -name "*_blastn_results.tsv"); do
        if [[ ! -s "$result" || $(head -n 1 "$result" | tr -d '\n') != "$results_header" ]]; then
            echo -e "$results_header" > temp_file
            cat "$result" >> temp_file
            mv temp_file "$result"
            python3 get_fasta_from_blast.py "$result" "$query".fasta
        fi
    done

    for result in $(find "$genome" -name "*_blastn_short_results.tsv"); do
        if [[ ! -s "$result" || $(head -n 1 "$result" | tr -d '\n') != "$results_header" ]]; then
            echo -e "$results_header" > temp_file
            cat "$result" >> temp_file
            mv temp_file "$result"
            python3 get_fasta_from_blast.py "$result" "$query".fasta
        fi
    done

    for result in $(find "$genome" -name "*_tblastx_results.tsv"); do
        if [[ ! -s "$result" || $(head -n 1 "$result" | tr -d '\n') != "$results_header" ]]; then
            echo -e "$results_header" > temp_file
            cat "$result" >> temp_file
            mv temp_file "$result"
            python3 get_fasta_from_blast.py "$result" "$query".fa
        fi
    done

    for combined in $(find "$genome" -name "*_blastn_results_combined*"); do
        mafft "$combined" > "${combined%.fasta}_aligned.fasta"
    done
    for combined in $(find "$genome" -name "*_blastn_short_results_combined*"); do
        mafft "$combined" > "${combined%.fasta}_aligned.fasta"
    done
    for combined in $(find "$genome" -name "*_tblastx_results_combined*"); do
        mafft "$combined" > "${combined%.fasta}_aligned.fasta"
    done

    for aligned in $(find "$genome" -name "*blastn_results*aligned*"); do
        cat "$aligned" >> "$blastn_combined"
    done
    for aligned in $(find "$genome" -name "*blastn_short_results*aligned*"); do
        cat "$aligned" >> "$blastn_short_combined"
    done
    for aligned in $(find "$genome" -name "*tblastx_results*aligned*"); do
        cat "$aligned" >> "$tblastx_combined"
    done
done

blastn_cleaned="${blastn_combined%.fasta}_cleaned.fasta"
blastn_short_cleaned="${blastn_short_combined%.fasta}_cleaned.fasta"
tblastx_cleaned="${tblastx_combined%.fasta}_cleaned.fasta"

python3 remove_duplicate_seqs.py "$blastn_combined" "$blastn_cleaned" "$query".fasta
python3 remove_duplicate_seqs.py "$blastn_short_combined" "$blastn_short_cleaned" "$query".fasta
python3 remove_duplicate_seqs.py "$tblastx_combined" "$tblastx_cleaned" "$query".fa


#generate trees



