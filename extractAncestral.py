#!/usr/bin/env python

import sys, re, os
from optparse import OptionParser

"""
Main Definitions
"""

def print_rec(rec):
    """
    Print a fasta record to stdout.
    """
    sys.stdout.write(">{}\n{}\n".format(rec["id"], rec["seq"]))
    return

def parse_rec(fh):
    """
    Parse a repeat record from an open file handle.
    Returns a dictionary.
    """
    rec = {
        'id': "",
        'class': "",
        'family': "",
        'species': "",
        'seq': "",
        'length': 0,
    }
    lines = []
    line_parts = []
    is_seq = False
    line = fh.readline()
    line_parts = line.split()
    while line != "" and line_parts[0] != "//":
        if is_seq:
            rec["seq"] = rec["seq"] + "".join(line_parts[0:-1])
        elif line_parts[0] == "ID":
            rec["id"] = line_parts[1]
            rec["length"] = line_parts[-2]
        elif line_parts[0] == "NM":
            # Catches proper ID from RepBase libraries
            rec["id"] = line_parts[1]
        elif line_parts[0] == "CC":
            if line_parts[1] == "Type:":
                if len(line_parts) > 2:
                    rec["class"] = line_parts[2]
            elif line_parts[1] == "SubType:":
                if len(line_parts) > 2:
                    rec["family"] = line_parts[2]
            elif line_parts[1] == "Species:":
                if len(line_parts) > 2:
                    rec["species"] = line_parts[2]
        elif line_parts[0] == "SQ":
            is_seq = True
        line = fh.readline()
        line_parts = line.split()
    return(rec)

if __name__ == "__main__":
    parser = OptionParser(description='Extract fasta of consensus sequences for the given repbase library.')
    parser.add_option('-s', '--seqs', type="string", default="",
                      help='Comma-delimited list of sequence names to extract.')

    (opt, args) = parser.parse_args(sys.argv)

    if opt.seqs != "":
        if os.path.isfile(opt.seqs):
            seqs_f = open(opt.seqs, "r")
            seqs = seqs_f.read().split('\n')
            #sys.stderr.write("{}\n".format(len(seqs)))
        else:
            seqs = opt.seqs.split(',')
    
    name = ""
    seq = ""
    is_seq_line = False
    infile = open(args[1])

    rec = parse_rec(infile)
    while rec["id"] != "":
        use_item = False
        if opt.seqs != "":
            use_item = False
            if rec["id"] in seqs:
                use_item = True            
        else:
            use_item = True
        if use_item:
            print_rec(rec)
        rec = parse_rec(infile)
