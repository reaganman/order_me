#!/bin/bash
#
# blast_em.sh - script for running blast searches and creating a compiled alignment of the hits.
#
# USAGE: bash blast_em.sh --Assemblies [assemblies_dir] --query [queryID] --blast_type [blastn, blastn_short, tblastx] --evalue [evalue] --merge_by [species, id] --output_alignment[name_to_save_alignment]
#
# Set the default merge option to "species"
merge_by=species

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key=$1
    case "$key" in
        --Assemblies)
            Assemblies=$2
            shift
            shift
            ;;
        --query)
            query=$2
            shift
            shift
            ;;
        --blast_type)
            blast_type=$2
            shift
            shift
            ;;
        --evalue)
            evalue=$2
            shift
            shift
            ;;
        --output_alignment)
            merged_fout=$2
            shift
            shift
            ;;
        --merge_by)
            merge_by=$2
            shift
            shift
            ;;
        *)
            echo "UNKNOWN OPTION $1"
            echo "USAGE: bash blast_em.sh --Assemblies [assemblies_dir] --query [queryID] --blast_type [blastn, blastn_short, tblastx] --evalue [evalue] --merge_by [species, id] --output_alignment[name_to_save_alignment]"
            exit 1
            ;;
    esac
done

# Load necessary modules
module load blast
module load mafft

# Run blast with the selected options
for species in $(find "$Assemblies" -type d); do
    # For each species with an assembly directory
    find "$species" -type f -name "*results*" -delete

    for fna_file in $(find "$species" -name '*.fna'); do
        # Find assemblies
        db_path="${fna_file%.fna}.db"
        echo "searching for ${query} in ${db_path} using ${blast_type}"

        if [[ "$blast_type" == "blastn" ]]; then
            blastn -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_"$query"_blastn_results.tsv
        fi

        if [[ "$blast_type" == "blastn_short" ]]; then 
            blastn -task "blastn-short" -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_"$query"_blastn_short_results.tsv
        fi

        if [[ "$blast_type" == "tblastx" ]]; then
            tblastx -query "$query".fasta -db "$db_path" -evalue "$evalue" -outfmt "6 stitle evalue pident sstart send qseqid qstart qend qseq sseq" -out "${db_path%.db}"_"$query"_tblastx_results.tsv
        fi
    done
done

# Compile blast results
results_compiled="${query}_aligned_${blast_type}_results.fasta"
rm -f "$results_compiled"  # Remove the combined file if it already exists

for species in $Assemblies; do
    species_dir=$(basename "$species")

    for result in $(find "$species" -name "*${query}_${blast_type}_results.tsv"); do
        if [[ -s "$result" ]]; then
            results_header="stitle\tevalue\tpident\tsstart\tsend\tqseqid\tqstart\tqend\tqseq\tsseq\n"
            echo "processing blast results for ${result}"

            # Make a fasta file for each blast hit with query sequences to align
            python3 get_fasta_from_blast.py "$result" "$results_header" "$query".fasta
        fi
    done

    for combined in $(find "$species" -name "*${query}_${blast_type}*_combined*"); do
        # Align hits to the query individually
        mafft "$combined" > "${combined%.fasta}_aligned.fasta"
    done

    for aligned in $(find "$species" -name "*${query}_${blast_type}_results*aligned*"); do
        # Compile aligned hits
        cat "$aligned" >> "$results_compiled"
    done
done

# Merge results based on the specified option (species or id)
case "$merge_by" in 
    "species")
        python3 merge_by_species.py "$results_compiled" "$merged_fout" "$query"
        ;;
    "id")
        python3 merge_by_id.py "$results_compiled" "$merged_fout" "$query"
        ;;
    *)
        echo "INVALID OPTION FOR --merge_by $merge_by"
        exit 1
        ;;
esac

#remove temporary alignments
rm *temp*



        