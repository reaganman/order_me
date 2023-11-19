from Bio import SeqIO
from Bio.Seq import Seq
from Bio import AlignIO
from Bio.Align.AlignInfo import SummaryInfo
from Bio.SeqRecord import SeqRecord
import sys


def consensus_by_species(input_file, output_file):
    records = list(SeqIO.parse(input_file, 'fasta'))
    species_records = {}
    for record in records:
        species = " ".join(record.description.split(" ")[1:3])
        if species not in species_records:
            species_records[species] = [record]
        else:
            species_records[species].append(record)


    merged_records = []
    for species, record_list in species_records.items():#get consensus alignment
        seq_ids=[]
        for record in record_list: #get sequence ids
            record_id = record.id
            if record_id not in seq_ids:
                seq_ids.append(record_id)
        temp_input_file = f"temp_input_{species}.fasta"
        SeqIO.write(record_list, temp_input_file, "fasta")
        alignment = AlignIO.read(temp_input_file, "fasta")
        summary_info = SummaryInfo(alignment)
        consensus_sequence = summary_info.dumb_consensus(threshold=0.51)
        consensus_id = species + " " + " + ".join(seq_ids)
        consensus_desription = species
        consensus_record = SeqRecord(consensus_sequence, id=consensus_id)
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

def remove_query(input_file, query_id):
    records_to_write = []
    records = list(SeqIO.parse(input_file, 'fasta'))[1:] # remove the query at the start
    for record in records: 
        if query_id not in record.id: 
            records_to_write.append(record)
    SeqIO.write(records_to_write, input_file, 'fasta')


if __name__ == '__main__':
    fin = sys.argv[1]
    fout = sys.argv[2]
    query = sys.argv[3]
    trimmed_fout = fin.rsplit('.')[0]+'_trimmed.fasta'
    trim_seqs(fin, trimmed_fout)
    remove_query(trimmed_fout, query)
    consensus_by_species(trimmed_fout, fout)


