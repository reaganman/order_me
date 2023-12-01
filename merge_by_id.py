from Bio import SeqIO
from Bio.Seq import Seq
from Bio import AlignIO
from Bio.Align.AlignInfo import SummaryInfo
from Bio.SeqRecord import SeqRecord
import sys


def consensus_by_id(input_file, output_file):
    """
    Generate a consensus sequence for each unique sequence ID in the input FASTA file.
    
    Parameters:
        input_file (str): Path to the input FASTA file containing sequences.
        output_file (str): Path to the output FASTA file to store consensus sequences.

    Returns:
        None
    """
    records = list(SeqIO.parse(input_file, 'fasta'))
    id_records = {}

    for record in records:
        seq_id = record.id
        if seq_id not in id_records:
            id_records[seq_id] = [record]
        else:
            id_records[seq_id].append(record)

    merged_records = []
    for seq_id, record_list in id_records.items():
        temp_input_file = f"temp_input_{seq_id}.fasta"
        SeqIO.write(record_list, temp_input_file, "fasta")
        alignment = AlignIO.read(temp_input_file, "fasta")
        summary_info = SummaryInfo(alignment)
        consensus_sequence = summary_info.dumb_consensus(threshold=0.51)
        consensus_id = seq_id + "_" + "consensus"
        consensus_description = record_list[0].description.split(',')[0] + " consensus sequence"
        consensus_record = SeqRecord(consensus_sequence, id=consensus_id, description=consensus_description)
        merged_records.append(consensus_record)

    SeqIO.write(merged_records, output_file, 'fasta')
    replace_x_with_gap(output_file, output_file)


def replace_x_with_gap(input_file, output_file):
    """
    Replace 'X' characters with '-' in sequences and write to a new FASTA file.

    Parameters:
        input_file (str): Path to the input FASTA file.
        output_file (str): Path to the output FASTA file with 'X' replaced by '-'.

    Returns:
        None
    """
    records = list(SeqIO.parse(input_file, "fasta"))
    for record in records:
        modified_seq = str(record.seq).replace("X", "-")
        record.seq = Seq(modified_seq)

    with open(output_file, 'w') as output_handle:
        SeqIO.write(records, output_handle, "fasta")


def pad_seqs(input_file, output_file):
    """
    Pad sequences with '-' to have equal length and write to a new FASTA file.

    Parameters:
        input_file (str): Path to the input FASTA file.
        output_file (str): Path to the output FASTA file with padded sequences.

    Returns:
        None
    """
    records = list(SeqIO.parse(input_file, "fasta"))
    max_length = max(len(record.seq) for record in records)
    padded_records = []
    for record in records:
        padding_length = max_length - len(record.seq)
        padded_seq = record.seq + Seq('-' * padding_length)
        padded_record = SeqRecord(padded_seq, id=record.id, description=record.description)
        padded_records.append(padded_record)

    SeqIO.write(padded_records, output_file, "fasta")


def remove_query(input_file, query_id):
    """
    Remove sequences containing the specified query ID and write to the same FASTA file.

    Parameters:
        input_file (str): Path to the input FASTA file.
        query_id (str): Identifier for the query sequence.

    Returns:
        None
    """
    records_to_write = []
    records = list(SeqIO.parse(input_file, 'fasta'))
    for record in records:
        if query_id not in record.id:
            records_to_write.append(record)
    SeqIO.write(records_to_write, input_file, 'fasta')


if __name__ == '__main__':
    fin = sys.argv[1]
    fout = sys.argv[2]
    query = sys.argv[3]
    trimmed_fout = fin.rsplit('.')[0] + '_trimmed.fasta'
    pad_seqs(fin, trimmed_fout)
    remove_query(trimmed_fout, query)
    consensus_by_id(trimmed_fout, fout)
