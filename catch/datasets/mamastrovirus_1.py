"""Dataset with 'Mamastrovirus 1' sequences.

A dataset with 31 'Mamastrovirus 1' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/mamastrovirus_1.fasta.gz", relative=True)
sys.modules[__name__] = ds