"""Dataset with 'Severe acute respiratory syndrome-related
coronavirus' sequences.

A dataset with 325 'Severe acute respiratory syndrome-related
coronavirus' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/severe_acute_respiratory_syndrome-related_coronavirus.fasta.gz", relative=True)
sys.modules[__name__] = ds