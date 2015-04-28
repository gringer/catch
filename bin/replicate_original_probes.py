#!/usr/bin/env python
"""Replicate probes generated by older code.

Designs probes to replicate those generated by the old Matlab code
and RemoveSimilarSequences.jar.
"""

import argparse
import importlib
import logging

from hybseldesign import coverage_analysis
from hybseldesign.filter import duplicate_filter
from hybseldesign.filter import naive_redundant_filter
from hybseldesign.filter import probe_designer
from hybseldesign.filter import reverse_complement_filter
from hybseldesign.utils import seq_io, version, log

__author__ = 'Hayden Metsky <hayden@mit.edu>'


def main(args):
    # Read the FASTA sequences
    try:
        dataset = importlib.import_module(
            'hybseldesign.datasets.' + args.dataset)
    except ImportError:
        raise ValueError("Unknown dataset %s" % ds)
    seqs = [seq_io.read_dataset_genomes(dataset)]

    # Setup the filters needed for replication
    # The filters needed for replication are, in order:
    #  1) Reverse complement (rc) -- add the reverse complement of
    #     each probe as a candidate
    rc = reverse_complement_filter.ReverseComplementFilter()
    #  2) Duplicate filter (df) -- condense all candidate probes that
    #     are identical down to one; this is not necessary for
    #     correctness, as the naive redundant filter achieves the same
    #     task implicitly, but it does significantly lower runtime by
    #     decreasing the input size to the naive redundant filter
    df = duplicate_filter.DuplicateFilter()
    #  3) Naive redundant filter (nf) -- execute a greedy algorithm to
    #     condense 'similar' probes down to one
    nf = naive_redundant_filter.NaiveRedundantFilter(
        naive_redundant_filter.redundant_shift_and_mismatch_count(
            shift=args.shift,
            mismatch_thres=args.mismatch_thres))
    filters = [rc, df, nf]

    # Design the probes
    # (including the replicate_first_version argument to execute
    #  bugs that were present in the code's prior version when
    #  generating the set of candidate probes)
    pb = probe_designer.ProbeDesigner(seqs, filters,
                                      replicate_first_version=True)
    pb.design()

    if args.print_analysis:
        analyzer = coverage_analysis.Analyzer(pb.final_probes,
                                              seqs,
                                              [args.dataset],
                                              mismatches=args.mismatch_thres)
        analyzer.run()
        analyzer.print_analysis()
    else:
        # Just print the number of probes
        print len(pb.final_probes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset",
                        required=True,
                        help="Label for the target dataset")
    parser.add_argument(
        "-s", "--shift",
        required=True,
        type=int,
        help=("Shift one probe from -shift to +shift bp relative to "
              "the other"))
    parser.add_argument(
        "-m", "--mismatch_thres",
        required=True,
        type=int,
        help=("Deem one probe redundant to another if, as one is "
              "shifted relative to the other, the minimum number of "
              "mismatches between them is <= 'mismatch_thres'"))
    parser.add_argument("--print_analysis",
                        dest="print_analysis",
                        action="store_true",
                        help="Print analysis of the probe set's coverage")
    parser.add_argument("--debug",
                        dest="log_level",
                        action="store_const",
                        const=logging.DEBUG,
                        default=logging.WARNING,
                        help=("Debug output"))
    parser.add_argument("--verbose",
                        dest="log_level",
                        action="store_const",
                        const=logging.INFO,
                        help=("Verbose output"))
    parser.add_argument('--version', '-V',
                        action='version',
                        version=version.get_version())
    args = parser.parse_args()

    log.configure_logging(args.log_level)
    main(args)