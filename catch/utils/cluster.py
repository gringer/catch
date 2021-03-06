"""Functions for clustering sequences before input.

This includes computing a distance matrix using MinHash, and
clustering that matrix.
"""

import ctypes
from collections import defaultdict
import logging
import multiprocessing
from multiprocessing import sharedctypes
import operator

import numpy as np
from scipy.cluster import hierarchy

from catch.utils import lsh

__author__ = 'Hayden Metsky <hayden@mit.edu>'

logger = logging.getLogger(__name__)


def make_signatures_with_minhash(family, seqs):
    """Construct a signature using MinHash for each sequence.

    Args:
        family: lsh.MinHashFamily object
        seqs: dict mapping sequence header to sequences

    Returns:
        dict mapping sequence header to signature
    """
    # Construct a single hash function; use the same for all sequences
    h = family.make_h()

    signatures = {}
    for name, seq in seqs.items():
        signatures[name] = h(seq)
    return signatures


def set_max_num_processes_for_creating_distance_matrix(max_num_processes=8):
    """Set the maximum number of processes to use for creating distance matrix.

    Args:
        max_num_processes: an int (>= 1) specifying the maximum number of
            processes to use in a multiprocessing.Pool when filling in the
            condensed distance matrix; it uses min(the number of CPUs in the
            system, max_num_processes) processes
    """
    global _cdm_max_num_processes
    _cdm_max_num_processes = max_num_processes
set_max_num_processes_for_creating_distance_matrix()


# Define variables and functions to use in a multiprocessing Pool for
# filling in the distance matrix; these must be top-level in the module
global _dist_matrix_shared
global _dist_fn
def _fill_in_for_j_range(args):
    j_start, j_end, n = args
    for j in range(j_start, j_end):
        for i in range(j):
            # Compute index in 1d vector for pair (i, j)
            idx = int((-1 * i*i)/2 + i*n - 3*i/2 + j - 1)
            # Fill in _dist_matrix_shared at idx
            _dist_matrix_shared[idx] = _dist_fn(i, j)

def create_condensed_dist_matrix(n, dist_fn, num_processes=None):
    """Construct a 1d condensed distance matrix for scipy.

    This fills in the matrix using a multiprocessing Pool. Note that having the
    processes call dist_fn will cause some memory copying: the function  refers
    to objects, which have reference counters that will be incremented (a
    write), and for subprocesses Unix performs a copy-on-write. This might
    cause a slowdown, but could be avoided in the future by copying the
    MinHash signatures into multiprocessing sharedtypes and having the distance
    function refer directly to these.

    Args:
        n: number of elements whose pairwise distances to store in the
            matrix
        dist_fn: function such that dist_fn(i, j) gives the distance
            between i and j, for all i<j<n
        num_processes: number of processes to use for the multiprocessing Pool;
            if not set, this determines a number

    Returns:
        condensed 1d distance matrix for input to scipy functions
    """
    global _cdm_max_num_processes
    if num_processes is None:
        num_processes = min(multiprocessing.cpu_count(),
                            _cdm_max_num_processes)

    # Define the global variable _dist_matrix_shared (this must be top-level
    # to be accessible by the top-level function _fill_in_for_j_range())
    logger.debug(("Setting up shared distance matrix"))
    global _dist_matrix_shared
    dist_matrix_len = int(n*(n-1)/2)
    _dist_matrix_shared = multiprocessing.sharedctypes.RawArray(
            ctypes.c_float, dist_matrix_len)

    # Define the global function _dist_fn (this must be top-level to be
    # used in a multiprocessing Pool)
    global _dist_fn
    _dist_fn = dist_fn

    num_pairs = n*(n-1) / 2
    logger.debug(("Condensed distance matrix has %d entries"), num_pairs)
    num_entries_per_process = int(num_pairs / num_processes)

    # Find out which value of j to start each process with
    logger.debug(("Assigning ranges in distance matrix to %d processes"),
            num_processes)
    j_start_for_process = [None for _ in range(num_processes)]
    num_entries_in_process = [0 for _ in range(num_processes)]
    process_num = 0
    j_start_for_process[process_num] = 0
    for j in range(n):
        if num_entries_in_process[process_num] >= num_entries_per_process:
            if process_num < num_processes - 1:
                # Move onto the next process
                process_num += 1
                j_start_for_process[process_num] = j
        # There are j entries associated with j
        num_entries_in_process[process_num] += j

    # Make arguments to _fill_in_for_j_range()
    args_for_process = []
    for process_num in range(num_processes):
        j_start = j_start_for_process[process_num]
        if j_start is None:
            # There are more processes than needed; stop filling in args
            break
        if process_num == num_processes - 1:
            j_end = n
        else:
            j_end = j_start_for_process[process_num + 1]
            if j_end is None:
                j_end = n
        args_for_process += [(j_start, j_end, n)]

    # Run the pool
    logger.debug(("Running multiprocessing pool to fill in distance matrix"))
    pool = multiprocessing.Pool(num_processes)
    pool.map(_fill_in_for_j_range, args_for_process)
    pool.close()

    # Convert back to numpy array
    logger.debug(("Converting shared distance matrix to numpy array"))
    dist_matrix = np.ctypeslib.as_array(_dist_matrix_shared)

    return dist_matrix


def cluster_from_dist_matrix(dist_matrix, threshold):
    """Use scipy to cluster a distance matrix.

    Args:
        dist_matrix: distance matrix, represented in scipy's 1d condensed form
        threshold: maximum inter-cluster distance to merge clusters (higher
            results in fewer clusters)

    Returns:
        list c such that c[i] is a collection of all the observations
        (whose pairwise distances are indexed in dist) in the i'th
        cluster, in sorted order by descending cluster size
    """
    linkage = hierarchy.linkage(dist_matrix, method='average')
    clusters = hierarchy.fcluster(linkage, threshold, criterion='distance')

    # clusters are numbered starting at 1, but base the count on
    # first_clust_num just in case this changes
    first_clust_num = min(clusters)
    num_clusters = max(clusters) + 1 - first_clust_num
    elements_in_cluster = defaultdict(list)
    for i, clust_num in enumerate(clusters):
        elements_in_cluster[clust_num].append(i)
    cluster_sizes = {c: len(elements_in_cluster[c])
                     for c in range(first_clust_num,
                                    num_clusters + first_clust_num)}

    elements_in_cluster_sorted = []
    for clust_num, _ in sorted(cluster_sizes.items(),
            key=operator.itemgetter(1), reverse=True):
        elements_in_cluster_sorted += [elements_in_cluster[clust_num]]
    return elements_in_cluster_sorted


def cluster_with_minhash_signatures(seqs, k=12, N=100, threshold=0.1):
    """Cluster sequences based on their MinHash signatures.

    Args:
        seqs: dict mapping sequence header to sequences
        k: k-mer size to use for k-mer hashes (smaller is likely more
            sensitive for divergent genomes, but may lead to false positives
            in determining which genomes are close)
        N: number of hash values to use in a signature (higher is slower for
            clustering, but likely more sensitive for divergent genomes)
        threshold: maximum inter-cluster distance to merge clusters, in
            average nucleotide dissimilarity (1-ANI, where ANI is
            average nucleotide identity); higher results in fewer
            clusters

    Returns:
        list c such that c[i] gives a collection of sequence headers
        in the same cluster, and the clusters in c are sorted
        in descending order of size
    """
    num_seqs = len(seqs)

    logger.info(("Producing signatures of %d sequences"), num_seqs)
    family = lsh.MinHashFamily(k, N=N)
    signatures_map = make_signatures_with_minhash(family, seqs)

    # Map each sequence header to an index (0-based), and get
    # the signature for the corresponding index
    seq_headers = []
    signatures = []
    for name, seq in seqs.items():
        seq_headers += [name]
        signatures += [signatures_map[name]]

    # Eq. 4 of the Mash paper (Ondov et al. 2016) shows that the
    # Mash distance, which is shown to be closely related to 1-ANI, is:
    #  D = (-1/k) * ln(2*j/(1+j))
    # where j is a Jaccard similarity. Solving for j:
    #  j = 1/(2*exp(k*D) - 1)
    # So, for a desired distance D in terms of 1-ANI, the corresponding
    # Jaccard distance is:
    #  1.0 - 1/(2*exp(k*D) - 1)
    # We can use this to calculate a clustering threshold in terms of
    # Jaccard distance
    jaccard_dist_threshold = 1.0 - 1.0/(2.0*np.exp(k*threshold) - 1)

    def jaccard_dist(i, j):
        # Return estimated Jaccard dist between signatures at
        # index i and index j
        return family.estimate_jaccard_dist(
            signatures[i], signatures[j])

    logger.info(("Creating condensed distance matrix of %d sequences"), num_seqs)
    dist_matrix = create_condensed_dist_matrix(num_seqs, jaccard_dist)
    logger.info(("Clustering %d sequences at Jaccard distance threshold of %f"),
            num_seqs, jaccard_dist_threshold)
    clusters = cluster_from_dist_matrix(dist_matrix,
        jaccard_dist_threshold)

    seqs_in_cluster = []
    for cluster_idxs in clusters:
        seqs_in_cluster += [[seq_headers[i] for i in cluster_idxs]]
    return seqs_in_cluster

