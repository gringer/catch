"""Dataset with 'Bhanja virus' sequences.

A dataset with 12 'Bhanja virus' sequences. The virus is segmented and
has 3 segments. Based on their strain and/or isolate, these sequences
were able to be grouped into 7 genomes. Many genomes may have fewer
than 3 segments.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

from os.path import dirname
from os.path import join
from os import listdir
import sys

from catch.datasets import GenomesDatasetMultiChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'

chrs = ["segment_" + seg for seg in ['L', 'M', 'S']]

def seq_header_to_chr(header):
    import re
    c = re.compile(r'\[segment (L|M|S)\]')
    m = c.search(header)
    if not m:
        raise ValueError("Unknown segment in header %s" % header)
    seg = m.group(1)
    valid_segs = ['L', 'M', 'S']
    if seg not in valid_segs:
        raise ValueError("Unknown segment %s" % seg)
    return "segment_" + seg


ds = GenomesDatasetMultiChrom(__name__, __file__, __spec__,
                              chrs, seq_header_to_chr)

for f in listdir(join(dirname(__file__), "data/bhanja/")):
    ds.add_fasta_path("data/bhanja/" + f, relative=True)

sys.modules[__name__] = ds
