from Bio import SeqIO
import argparse
import os
import sys

def split_fasta(input_multi_file, input_single_file, output_dir):
    """
    Split a multiple-sequence FASTA file and a single-sequence FASTA file into individual files.

    Parameters:
        input_multi_file (str): Path to the multiple-sequence FASTA file.
        input_single_file (str): Path to the single-sequence FASTA file.
        output_dir (str): Path to the directory for individual files.

    Returns:
        None
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read multiple-sequence FASTA file
    sequences_multi = list(SeqIO.parse(input_multi_file, "fasta"))

    # Read single-sequence FASTA file
    sequence_single = list(SeqIO.parse(input_single_file, "fasta"))

    # Write individual FASTA files for each sequence from the multiple-sequence file
    for index, seq_multi in enumerate(sequences_multi, start=1):
        output_file = os.path.join(output_dir, f'sequence_{index}_pair.fasta')
        SeqIO.write([seq_multi] + sequence_single, output_file, "fasta")

def parse_arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Split a multiple-sequence and a single-sequence FASTA file into individual files.")
    parser.add_argument("input_multi_file", help="Path to the multiple-sequence FASTA file.")
    parser.add_argument("input_single_file", help="Path to the single-sequence FASTA file.")
    parser.add_argument("output_dir", help="Path to the directory for individual files.")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Check if input files exist
    for input_file in [args.input_multi_file, args.input_single_file]:
        if not os.path.isfile(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            sys.exit(1)

    # Call the split_fasta function
    split_fasta(args.input_multi_file, args.input_single_file, args.output_dir)

    print("Splitting completed successfully.")

