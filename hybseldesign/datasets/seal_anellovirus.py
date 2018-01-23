"""Dataset with 'Seal anellovirus( TFFN/USA/2006| [0-9]+)?' sequences.

A dataset with 2 'Seal anellovirus( TFFN/USA/2006| [0-9]+)?' genomes.

THIS PYTHON FILE WAS GENERATED BY A COMPUTER PROGRAM! DO NOT EDIT!
"""

import sys

from catch.datasets import GenomesDatasetSingleChrom

__author__ = 'Hayden Metsky <hayden@mit.edu>'


ds = GenomesDatasetSingleChrom(__name__, __file__, __spec__)
ds.add_fasta_path("data/seal_anellovirus.fasta", relative=True)
sys.modules[__name__] = ds
