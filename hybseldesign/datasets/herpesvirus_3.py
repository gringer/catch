"""Dataset with 'Human alphaherpesvirus 3' sequences.

A dataset with 81 'Human alphaherpesvirus 3' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/herpesvirus_3.fasta", relative=True)
sys.modules[__name__] = ds
