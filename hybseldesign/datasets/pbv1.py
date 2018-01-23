"""Dataset with 'Primate bocaparvovirus 1' sequences.

A dataset with 5 'Primate bocaparvovirus 1' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/pbv1.fasta", relative=True)
sys.modules[__name__] = ds
