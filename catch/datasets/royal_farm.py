"""Dataset with 'Royal Farm virus' sequences.

A dataset with 4 'Royal Farm virus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/royal_farm.fasta.gz", relative=True)
sys.modules[__name__] = ds
