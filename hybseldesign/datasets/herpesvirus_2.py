"""Dataset with 'Human alphaherpesvirus 2' sequences.

A dataset with 38 'Human alphaherpesvirus 2' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/herpesvirus_2.fasta", relative=True)
sys.modules[__name__] = ds
