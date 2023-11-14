from Bio import Entrez
import os
import subprocess
import argparse

def download_genomes_for_order(taxid, email, save_path):
    Entrez.email = email

    # Set the batch size and initial start index
    retmax = 500
    retstart = 0

    # Create a directory for the order
    order_directory = os.path.join(save_path, f"Genomes_{taxid}")
    if not os.path.exists(order_directory):
        os.makedirs(order_directory)

    while True:
        # Search for the genomes associated with the specified taxid
        search_term = f"txid{taxid}[Organism] AND latest[filter] AND (latest_refseq[filter] OR latest_genbank[filter])"
        handle = Entrez.esearch(db="assembly", term=search_term, retmax=retmax, retstart=retstart)
        record = Entrez.read(handle)
        id_list = record["IdList"]

        if len(id_list) == 0:
            break

        # Fetch the FTP paths for the genomes and download all available files
        for genome_id in id_list:
            handle = Entrez.esummary(db="assembly", id=genome_id)
            record = Entrez.read(handle)
            ftp_path = record["DocumentSummarySet"]["DocumentSummary"][0]["FtpPath_GenBank"]
            organism_name = record["DocumentSummarySet"]["DocumentSummary"][0]["AssemblyName"]
            directory_name = os.path.join(order_directory, organism_name.replace(" ", "_"))
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)
            os.chdir(directory_name)
            download_command = f"wget -r -nd -A '*' {ftp_path}"
            subprocess.call(download_command, shell=True)
            os.chdir('..')

        retstart += retmax

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download genomes for a specified order from NCBI.')
    parser.add_argument('--taxid', type=int, required=True, help='Taxonomic identifier for the order')
    parser.add_argument('--email', type=str, required=True, help='Your email address')
    parser.add_argument('--save_path', type=str, required=True, help='Path to save the order directory')
    args = parser.parse_args()

    download_genomes_for_order(args.taxid, args.email, args.save_path)

