# bash test_order_me.sh --save_path /scratch/general/nfs1/utu_4310/fr10_evolution_wd/test_get_genomes --query U44831 --taxid 8342 --email reagan.mckee@utahtech.edu


#load environment
query=''
taxid=''
email=''


module load blast
module load mafft
module load iqtree

#set default values
save_path=$(pwd)
evalue=0.0001
blast_type=blastn_short


#get arguments
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
            echo "UNKOWN OPTION: $1"
            echo "USAGE: bash order_me.sh --query <query> --taxid <taxid> --email <email> [other options...]"
            exit 1
            ;;
    esac
done

if [[ ! "$query" || ! "$taxid" || ! "$email" ]]; then 
    echo "USAGE: bash order_me.sh --query <query> --taxid <taxid> --email <email> [other options...]"
    exit 1
fi

log="$query"_in_"$taxid"_log.txt


#download and translate query
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=$query&rettype=fasta&retmode=text" > "$query".fasta
python3 get_translation.py "$query".fasta "$query".fa


if [[ "$setup" ]]; then #setup blast
    echo "downloading assemblies and making blast dbs!"
    bash setup_blast.sh --save_path "$save_path" --taxid "$taxid" --email "$email"
fi


#run blast and merge results
Assemblies="$save_path"/Assemblies_"$taxid"/
final_aligned_results="$query"_in_"$taxid"_"$blast_type".fasta
bash blast_em.sh --Assemblies "$Assemblies" --query "$query" --blast_type "$blast_type" --evalue "$evalue" --output_alignment "$final_aligned_results"


echo "Alignment created: $final_aligned_results"
echo "Check alignment then generate consensus tree with: bash make_tree.sh $final_aligned_results"

#generate tree

#bash make_tree.sh "$final_aligned_results"



