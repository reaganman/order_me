while [[ $# -gt 0 ]]; do #parse arguments
    key=$1

    case "$key" in 
        --save_path)
            save_path=$2
            shift
            shift
            ;;
        --taxid)
            taxid=$2
            shift 
            shift
            ;;
        --email)
            email=$2
            shift
            shift
            ;;
        --query
            query=$2
            shift
            shift
            ;;
        *)
            echo "UNKNOWN OPTION: $1"
            echo "USAGE: bash setup_blast.sh --save_path --taxid --query"
            exit 1
            ;;
    esac
done

if [[ ! "$save_path" || ! "$taxid" ]]; then
    echo "USAGE: bash setup_blast.sh --save_path <path> --taxid <taxid>"
    exit 1
fi


#download assemblies
python3 get_genomes.py --taxid $taxid --email $email --save_path $save_path
Assemblies="$save_path"/Assemblies_"$taxid"/*

#unzip the fnas
for assembly in $Assemblies; do
	gunzip "$assembly"/*fna.gz;
done

#make blast dbs
for assembly in $Assemblies; do
   for fna_file in $(find "$assembly" -name '*.fna'); do
       makeblastdb -dbtype nucl -in "$fna_file" -out "${fna_file%.fna}.db"
   done
done