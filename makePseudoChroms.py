import sys, re, os
from argparse import ArgumentParser
from Bio import SeqIO

if __name__ == "__main__":
    parser = ArgumentParser(description='Extract fasta of consensus sequences for the given repbase library.')
    parser.add_argument('seq_file', metavar='FILE', type=str,
                        help='Fasta sequences to concatenate into pseudochromosome(s).')
    parser.add_argument('out_file', metavar='OUTFILE', type=str,
                        help='File to write pseudochromosome sequence(s) to. (FASTA format)')
    parser.add_argument('index_file', metavar='INDEXFILE', type=str,
                        help='File to which coordinates of input sequences within pseudochromosome(s) will be written. (BED format)')
    parser.add_argument('-n', '--n-chroms', dest='n_chroms', metavar='N', type=int, default=20,
                        help='Number of pseudochromosomes to produce. Default = 20.')
    parser.add_argument('-l', '--spacer-len', dest='spacer_len', type=int, default=1000,
                        help='Spacer sequence length. Default = 1000')
    parser.add_argument('-s', '--spacer', metavar='SPACER_SEQ', type=str, default="a",
                        help='Spacer sequence to use. This will be repeated a number of times to equal the spacer length. Default = "a"')

    args = parser.parse_args()


    # Produce the spacer sequence by repeating the spacer to produce a sequence
    # of the specified length.
    spacer_seq = ""
    while len(spacer_seq) < args.spacer_len:
        spacer_seq = spacer_seq + args.spacer
        
    # Iterate over sequences in the input file and build a list of N pseudochrom
    # sequences by sequentially concatenating input sequences and spacers to a
    # list of strings.
    seqs = []
    for i in range(0,args.n_chroms):        
        seqs.append("")
    idx = 0
    f = open(args.index_file, "w+")
    with open(args.seq_file, "rU") as fasta:
        for record in SeqIO.parse(fasta, "fasta"):
            if idx > args.n_chroms - 1:
                idx = 0
            start = len(seqs[idx])
            seqs[idx] = seqs[idx] + record.seq
            end = len(seqs[idx])
            seqs[idx] =	seqs[idx] + spacer_seq
            f.write("chr{}\t{}\t{}\t{}\n".format(idx+1, start, end, record.id))
            idx += 1
    f.close()
    
    # Write the chromosomes as fasta sequences to the output file
    f = open(args.out_file, "w+")
    for	idx in range(0,args.n_chroms):
        f.write(">chr{}\n".format(idx+1))
        f.write("{}\n".format(seqs[idx]))
    f.close()
