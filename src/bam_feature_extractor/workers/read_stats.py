import math
from collections import Counter

from pysam import AlignmentFile
from tqdm import tqdm

from bam_feature_extractor.core.report import Report
from bam_feature_extractor.core.worker import Worker

# split the reference in regions of equal sizes
REGION_NUMBER = 100
# length of subsequences used in complexity/entropy computation
SUB_SEQUENCE_LENGTHS = (2, 3, 4, 5, 6, 7, 8)


class ReadsStats(Worker):
    description = """
    Compute statistics on reads
    
    - sequence
    - sequence length
    - number of occurence for each base A,T,C,G
    - ratio GC: (G + C) / length(sequence)
    - normalized shanon entropy: normalized by maximal entropy for a sequence of its length
    - complexity: 
        given a subsequence size (N):
        - compute the effective number of distinct subsequences in the read
        - compute the maximal possible number of distinct subsequence of size N in the read
        - the result for N is the ratio (in percentage %) of those two values 
    
    Example:
TTTTGCAGTTCCCATTGACATTCCAATTTGGGGGTGGTAGTAGTGGAGAGACAGCATTTGAAATGTCCATTATGTGGTGGAACGGATTTTCAAGTTGAGGAGGGTAAGCTTGACAGCAAGTGGGGGTTTACGGCTCACAAAGTTAAGATAGTCATCTGCAAGAACTGCGGTTATGTTATGATGTTCTACAAAGGGAGAACCATCTGGGATTTTGATTAAAACAAGCGTTAAGGTTTATATTTGGACACTTTAATGTACTCTGGGGATGAAAAATGATTGAACGCTTAAAGCAGATGCTCCGGGTTGAGGTAATAGGTGTTGAAATACTCAGGGAACAGGTATCCTGTATGCCGAAGGGGTCAGGGGTAGAATTGCTGTTGGAAGTGGAGGTTCTGCTGTAAAAGCTGCGGAGCTTGTCTTAGGAAAAAAGATTGAAATCAGGGGGAGATAGTTTTGATTAAAGATTTTAAAAGGCAGGAGCTTGAAGACTTAGCGATCTCATATATAGTCCTGCTGATTCTGTTTTCGAACTTCGAGATAAAGAACATGCCATACGTGGCTTTGGCTGTCTTGACAGCTTTTGTTTTCCATGAGCTGGCTCACAGGCAGGTTGAAAGATGTATTGATAATAGCATATACAAGCAGTGGATAGCCAGATGTAATAGCTCTCCTGTTCACATAGCTGGAGAATAATCTGGTCATGCGATATTTTTTTCCCAACAACTGAAGTCTTCGCTGTACCCTACAGTTCTGGGAAGATAGGAAAACAGAAGGATAATCACTATATCAACCATAACAAACATAATAACTTGGAATCCTACTGGTGTGAGAAAGCGTTCTGGCTTCCCGCTTCATGCACTGATATCTTTATTCTACACCGCAATAGTGAACTTCTGGATAGCGTTCTTCAACCTTTTGCCGTTTCCACCTCTTGATGGCTACAAAGTTCTCAAGTGGAACGCTGGTTATTGGGCTGTTGCAATTGGGATAGCGTATGTTCTAAGGTCTCTGGTCTGATTCTTTTAACACCTTTA
length: 1034
ATCG: [288, 314, 174, 258]
ratio GC: 41.8%
normalized shanon entropy: 98.40807788014543
complexity (2, 3, 4, 5, 6, 7, 8): [100, 100, 91, 56, 83, 94, 98]
    
    """

    def build_report(self, data: AlignmentFile, report: Report):
        lines = [
            self.reference_report(data, ref)
            for ref in data.references
        ]
        report.features['reads'] = '\n'.join(lines)

    def reference_report(self, data: AlignmentFile, ref: str):
        stats = data.get_index_statistics()[data.get_tid(ref)]
        reads_number = stats.total
        if reads_number == 0:
            return ''

        res = []
        reads = list(data.fetch(ref))
        for read in tqdm(reads[:1000]):
            sequence = read.query_sequence
            cigar_stats = read.get_cigar_stats()
            sequence_length = len(sequence)
            a, t, c, g = atcg = list(map(sequence.count, list('ATCG')))

            res.extend([
                sequence,
                f'length: {sequence_length}',
                f'ATCG: {atcg}',
                f'ratio GC: {100 * (g + c) / sequence_length:.1f}%',
                f'normalized shanon entropy: {normalized_shannon_entropy(sequence)}',
                f'complexity {SUB_SEQUENCE_LENGTHS}: {[sequence_complexity(sequence, _) for _ in SUB_SEQUENCE_LENGTHS]}',
            ])

        lines = [
            f'[{ref}]',
            *res
        ]
        return '\n'.join(map(str, lines))


def normalized_shannon_entropy(sequence: str, k: int = 1):
    # Calculer la fréquence de chaque base dans la séquence

    kmers = [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
    freq = Counter(kmers)
    length = len(kmers)

    # Calculer l'entropie de Shannon
    entropy = 0.0
    for count in freq.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    max_entropy = math.log2(len(freq))
    return 100 * entropy / max_entropy


def sequence_complexity(sequence: str, k=2):
    # Calculer le nombre de k-mers (motifs de longueur k) dans la séquence
    kmers = [sequence[i:i + k] for i in range(len(sequence) - k + 1)]

    unique_kmers = set(kmers)
    max_kmers = min(len(kmers), 4 ** k)
    unique_kmers_number = len(unique_kmers)

    complexity = unique_kmers_number / max_kmers

    return math.floor(100 * complexity)
