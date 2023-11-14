import sys
from Bio import SeqIO
from Bio.Seq import Seq

def find_longest_orf(sequence):
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]

    max_orf = ""
    max_orf_length = 0

    for frame in range(3):
        current_orf = ""
        i = frame

        while i < len(sequence) - 2:
            codon = sequence[i:i + 3]

            if codon == start_codon:
                current_orf += codon
                i += 3

                while i < len(sequence) - 2:
                    codon = sequence[i:i + 3]
                    current_orf += codon

                    if codon in stop_codons:
                        if len(current_orf) > max_orf_length:
                            max_orf = current_orf
                            max_orf_length = len(current_orf)
                        break

                    i += 3
            else:
                i += 3

    return max_orf

def translate_and_write_to_file(input_file, output_file):
    # Read FASTA sequence
    record = SeqIO.read(input_file, "fasta")
    sequence = str(record.seq)

    # Find and translate the longest ORF
    longest_orf = find_longest_orf(sequence)
    translated_sequence = Seq(longest_orf).translate()

    # Remove everything after the first "*"
    translated_sequence = translated_sequence.split("*")[0]

    # Write the results to the output file
    with open(output_file, "w") as out_file:
        out_file.write(f">{record.id}\n")
        out_file.write(str(translated_sequence))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.fasta output.fa")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_fa = sys.argv[2]

    translate_and_write_to_file(input_fasta, output_fa)

