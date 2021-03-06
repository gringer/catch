"""Dataset with 'Human mastadenovirus D' sequences.

A dataset with 195 'Human mastadenovirus D' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/human_mastadenovirus_d.fasta.gz", relative=True)
sys.modules[__name__] = ds
