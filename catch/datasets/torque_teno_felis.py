"""Dataset with 'Torque teno felis virus' sequences.

A dataset with 8 'Torque teno felis virus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/torque_teno_felis.fasta.gz", relative=True)
sys.modules[__name__] = ds