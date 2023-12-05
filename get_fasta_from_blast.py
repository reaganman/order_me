import sys
import pandas as pd
import argparse

def make_tsv(results_file, header, outfile):
    """
    Extracts non-header lines from the BLAST results file and writes them to a new TSV file.

    Parameters:
        results_file (str): Path to the BLAST results file.
        header (str): Header line to be excluded from the new TSV file.
        outfile (str): Path to the output TSV file.
    """
    not_header = [header]
    with open(results_file, 'r') as results:
        lines = results.readlines()
        for line in lines:
            if line.strip() != header:
                not_header.append(line)

    with open(outfile, 'w') as results_out:
        for line in not_header:
            results_out.write(line)

def make_fasta(in_file, query_file):
    """
    Reads a TSV file with BLAST results and a query FASTA file, then creates FASTA files for each hit.

    Parameters:
        in_file (str): Path to the input TSV file with BLAST results.
        query_file (str): Path to the query FASTA file.
    """
    df = pd.read_csv(in_file, sep='\t')

    with open(query_file, 'r') as query:
        query_fasta = query.read().rstrip('\n') + '\n'

    stitle = df.stitle
    sstart = df.sstart
    send = df.send
    evalue = df.evalue
    pident = df.pident
    sseq = df.sseq
    qseqid = df.qseqid
    qstart = df.qstart
    qend = df.qend
    qseq = df.qseq

    for i, line in enumerate(stitle):
        seqs = []
        subject_header = f">{stitle[i]}_{sstart[i]}_{send[i]}_{evalue[i]}_{pident[i]}\n"
        subject_hit = f"{sseq[i]}\n"
        subject_seq = subject_header + subject_hit

        query_header = f">{qseqid[i]}_{qstart[i]}_{qend[i]}\n"
        query_hit = f"{qseq[i]}\n"
        query_seq = query_header + query_hit

        seqs.append(query_seq)
        seqs.append(subject_seq)

        if len(seqs) != 0:
            temp_seqs = [query_fasta]
            temp_seqs += seqs
            seqs = temp_seqs

            filename_without_extension = in_file.rsplit('.', 1)[0]
            out_file = f"{filename_without_extension}_combined_{i}.fasta"
            with open(out_file, 'w') as fout:
                fout.writelines(seqs)

def main():
    """
    Parse command-line arguments and execute script.
    """
    parser = argparse.ArgumentParser(description='Process BLAST results and create FASTA files for each hit.')
    parser.add_argument('results_file', type=str, help='Path to the BLAST results file.')
    parser.add_argument('header', type=str, help='Header line to be used in the new TSV file.')
    parser.add_argument('query_file', type=str, help='Path to the query FASTA file.')
    args = parser.parse_args()

    results_tsv = args.results_file.rsplit('.', 1)[0] + "_formatted.tsv"
    header = args.header.encode('utf-8').decode('unicode_escape')

    make_tsv(args.results_file, header, results_tsv)
    make_fasta(results_tsv, args.query_file)

if __name__ == "__main__":
    main()
