from Bio import SeqIO
from Bio.Seq import Seq
from Bio import AlignIO
from Bio.Align.AlignInfo import SummaryInfo
from Bio.SeqRecord import SeqRecord
import sys

def consensus_by_id(input_file, output_file):
    records = list(SeqIO.parse(input_file, 'fasta'))
    id_records = {}
    for record in records:
        seq_id = record.id
        if seq_id not in id_records:
            id_records[seq_id] = [record]
        else:
            id_records[seq_id].append(record)

    merged_records = []
    for seq_id, record_list in id_records.items(): #get consensus alignment
        temp_input_file = f"temp_input_{seq_id}.fasta"
        SeqIO.write(record_list, temp_input_file, "fasta")
        alignment = AlignIO.read(temp_input_file, "fasta")
        summary_info = SummaryInfo(alignment)
        consensus_sequence = summary_info.dumb_consensus(threshold=0.51)
        consensus_id = seq_id+"_"+"consensus"
        consensus_desription = record_list[0].description.split(',')[0] + " concensus sequence"
        consensus_record = SeqRecord(consensus_sequence, id=consensus_id, description=consensus_desription)
        merged_records.append(consensus_record)

        SeqIO.write(merged_records, output_file, 'fasta')
        replace_x_with_gap(output_file, output_file)

def replace_x_with_gap(input_file, output_file):
    records = list(SeqIO.parse(input_file, "fasta"))
    for record in records:
    # Convert the sequence to a string, replace "X" with "-", and create a new Seq object
        modified_seq = str(record.seq).replace("X", "-")
        record.seq = Seq(modified_seq)

    # Write the modified sequences to the output file
    with open(output_file, 'w') as output_handle:
        SeqIO.write(records, output_handle, "fasta")

def trim_seqs(input_file, output_file):
    records = list(SeqIO.parse(input_file, "fasta"))
    min_length = min(len(record.seq) for record in records)
    trimmed_records = [record[:min_length] for record in records]
    SeqIO.write(trimmed_records, output_file, "fasta")

if __name__ == '__main__':
    fin = sys.argv[1]
    trimmed_fout = fin.rsplit('.')[0]+'_trimmed.fasta'
    trim_seqs(fin, trimmed_fout)
    merged_fout = trimmed_fout.rsplit('.')[0]+'_merged.fasta'
    consensus_by_id(trimmed_fout, merged_fout)



