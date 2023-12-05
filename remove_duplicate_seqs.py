from Bio import SeqIO
import argparse

def remove_duplicates_by_id(input_file, output_file):
    """
    Remove duplicate sequences based on sequence identifiers (IDs) from a FASTA file.

    Parameters:
        input_file (str): Path to the input FASTA file.
        output_file (str): Path to the output FASTA file without duplicates.

    Returns:
        None
    """
    sequences = list(SeqIO.parse(input_file, 'fasta'))
    unique_sequences = {seq.id: seq for seq in sequences}

    # Write unique sequences to the output file
    SeqIO.write(list(unique_sequences.values()), output_file, 'fasta')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate sequences based on sequence identifiers (IDs) from a FASTA file.")
    parser.add_argument("input_file", help="Path to the input FASTA file.")
    parser.add_argument("output_file", help="Path to the output FASTA file without duplicates.")

    args = parser.parse_args()

    # Call the remove_duplicates_by_id function
    remove_duplicates_by_id(args.input_file, args.output_file)

