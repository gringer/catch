"""Dataset with 'Human herpesvirus 5' sequences.

A dataset with 153 'Human herpesvirus 5' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from hybseldesign.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/herpesvirus_5.fasta", relative=True)
sys.modules[__name__] = ds