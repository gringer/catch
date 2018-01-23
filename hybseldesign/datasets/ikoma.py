"""Dataset with 'Ikoma lyssavirus' sequences.

A dataset with 1 'Ikoma lyssavirus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/ikoma.fasta", relative=True)
sys.modules[__name__] = ds
