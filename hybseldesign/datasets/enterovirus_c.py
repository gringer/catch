"""Dataset with 'Enterovirus C' sequences.

A dataset with 443 'Enterovirus C' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/enterovirus_c.fasta", relative=True)
sys.modules[__name__] = ds
