from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import argparse

def remove_gaps(input_file, output_file, target_sequence_id):
    """
    Remove positions with gaps in the target sequence from the alignment.

    Parameters:
        input_file (str): Path to the input FASTA alignment file.
        output_file (str): Path to the output FASTA alignment file without gaps.
        target_sequence_id (str): Identifier for the target sequence.

    Returns:
        None
    """
    sequences = list(SeqIO.parse(input_file, 'fasta'))

    # Find the target sequence
    target_sequence = next(seq for seq in sequences if seq.id == target_sequence_id)

    # Find positions with gaps in the target sequence
    positions_with_gaps = [i for i, base in enumerate(target_sequence.seq) if base == '-']

    # Remove positions with gaps from all sequences
    for seq in sequences:
        seq.seq = Seq(''.join([base for i, base in enumerate(seq.seq) if i not in positions_with_gaps]))

    # Write modified alignment to the output file
    SeqIO.write(sequences, output_file, 'fasta')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove positions with gaps in the target sequence from a FASTA alignment.")
    parser.add_argument("input_file", help="Path to the input FASTA alignment file.")
    parser.add_argument("output_file", help="Path to the output FASTA alignment file without gaps.")
    parser.add_argument("target_sequence_id", help="Identifier for the target sequence.")

    args = parser.parse_args()

    # Call the remove_gaps function
    remove_gaps(args.input_file, args.output_file, args.target_sequence_id)
