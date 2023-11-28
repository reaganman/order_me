import sys
import pandas as pd

def make_tsv(results_file, header, outfile):
        not_header=[header]
        with open(results_file, 'r') as results:
            lines = results.readlines()
            for line in lines:
                if line.strip() != header:
                    print(f"line: {line}")
                    print(f"header: {header}")
                    not_header.append(line)
        with open(outfile, 'w') as results:
            for line in not_header:
                print(f"line to write: {line}")
                results.write(line)
        

def make_fasta(in_file, query_file):
    df = pd.read_csv(in_file, sep='\t')

    with open(query_file, 'r') as query:
        query_fasta = query.read().rstrip('\n')+'\n'

    stitle = df.stitle
    sstart = df.sstart
    send = df.send
    evalue = df.evalue
    pident = df.pident
    sseq = df.sseq
    qseqid = df.qseqid
    qstart=df.qstart
    qend = df.qend
    qseq = df.qseq

    for i, line in enumerate(stitle):
        seqs = []
        subject_header = ">"+stitle[i]+"_"+str(sstart[i])+"_"+str(send[i])+"_"+str((evalue[i]))+"_"+str(pident[i])+"\n"
        subject_hit = sseq[i] + "\n"
        subject_seq = subject_header + subject_hit
        query_header = ">"+qseqid[i]+"_"+str(qstart[i])+"_"+str(qend[i])+"\n"
        query_hit = qseq[i] + "\n"
        query_seq = query_header + query_hit
        seqs.append(query_seq)
        seqs.append(subject_seq)
        if len(seqs)!=0:
            temp_seqs=[query_fasta]
            temp_seqs+=seqs
            seqs=temp_seqs
        #write to output
            filename_without_extension = in_file.rsplit('.', 1)[0]
            out_file = f"{filename_without_extension}_combined_{i}.fasta"
            with open(out_file, 'w') as fout:
                for j in seqs:
                    fout.write(j)



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: get_fasta_from_blast.py results_file.tsv header query.fasta")
        sys.exit(1)

    blast_results = sys.argv[1]
    results_tsv = blast_results.rsplit('.', 1)[0]+"_formated.tsv"
    header = sys.argv[2].encode('utf-8').decode('unicode_escape')
    query = sys.argv[3]

    make_tsv(blast_results, header, results_tsv)

    make_fasta(results_tsv, query)














