#script for running blast searches and creating a compiled alignment of the hits
#example usage: bash blast_em.sh 
Genomes=$1 #/scratch/general/nfs1/utu_4310/fr10_evolution_wd/test_get_genomes/Genomes_8342/*
query=$2 #U44831
blast_type=$3 #blastn_short
evalue=$4 #.0001
merged_fout=$5 #"$query"_in_8342.fasta
log="$query"_blast_em_log.txt

module load blast
module load mafft

#run blast with selected option
for genome in $Genomes; do  #look in each genome
    find "$genome" -type f -name "*results*" -delete
    for fna_file in $(find "$genome" -name '*.fna'); do #find all blastdbs
	db_path="${fna_file%.fna}.db"
	dir_name=$(basename "$genome")
	echo "running blast with ${db_path}"
        if [[ "$blast_type" == "blastn" ]]; then
            blastn -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_blastn_results.tsv;
        fi

        if [[ "$blast_type" == "blastn_short" ]]; then 
            blastn -task "blastn-short" -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_"${blast_type}"_results.tsv;
        fi

        if [[ "$blast_type" == "tblastx" ]]; then
                tblastx -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_tblastx_results.tsv;
        fi;
    done;
done


# #compile blast results
results_compiled="aligned_${blast_type}_results.fasta"
rm -f "$results_combined"  # Remove the combined file if it already exists
for genome in $Genomes; do
    genome_name=$(basename "$genome")
    find "$genome" -type f -name "*combined*" -delete
    find "$genome" -type f -name "*fasta*" -delete
    echo "$genome_name" >> "$log"


    for result in $(find "$genome" -name "*_${blast_type}_results.tsv"); do
        if [[ -s "$result" ]]; then
            results_header="stitle\tevalue\tpident\tsstart\tsend\tqseqid\tqstart\tqend\tqseq\tsseq\n"
            echo "processing blast results for ${genome}"
            python3 get_fasta_from_blast.py "$result" "$results_header" "$query".fasta #make fasta for each blastn hit with query and hit sequences to align
        fi;
    done;

    for combined in $(find "$genome" -name "*_${blast_type}*_combined*"); do #align idividual hits 
            mafft "$combined" > "${combined%.fasta}_aligned.fasta";
        done;

    for aligned in $(find "$genome" -name "*${blast_type}_results*aligned*"); do
        cat "$aligned" >> "$results_compiled";
    done;
done

python3 merge_by_species.py "$results_compiled" "$merged_fout" "$query"
        