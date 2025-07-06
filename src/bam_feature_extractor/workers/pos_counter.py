from collections import Counter

from pysam import AlignmentFile

from bam_feature_extractor.core.report import Report
from bam_feature_extractor.core.worker import Worker


class PosCounter(Worker):
    description = """
    For each sequence (read), get the list of reference positions.
    For exemple the CGTAB sequence could be aligned at positions [1, 4, 100, 200].

    We compute the following stats :
    - pos_stats : the number of sequence aligned at a specific position,
    - sequence_stats: the number of alignment for each sequence.
    
    
    Example (pos_stats):
    The following means:
        - there is 6000 sequences aligned at position 300,
        - there is 3 sequences aligned at position 0.

300: 6000
0: 3
    
    
    Example (sequence_stats):
    The following means the sequence 'GTGTGCTT...':
        - is of length 2513
        - the CGAT bases are present [19.1%, 25.5%, 28.4%, 27.0%] in the sequence
        - is aligned at 9073 different positions
        

GTGTGCTT...
CGAT = [ 19.1, 25.5, 28.4, 27.0] length=2513
9073

    """

    def build_report(self, data: AlignmentFile, report: Report):

        block_size = 100

        pos_stats = Counter()
        sequence_stats = Counter()

        for idx, _ in enumerate(data.fetch(until_eof=True)):
            sequence_stats[_.query_sequence] = len(_.get_reference_positions())

            for pos in _.get_reference_positions():
                block_pos = (pos // block_size) * block_size
                pos_stats[block_pos] += 1

        report.features['pos_stats'] = '\n'.join([
            f'{k:10}: {v}'
            for k, v in pos_stats.most_common()
        ])

        report.features['sequence_stats'] = '\n'.join([
            f'{k}\n{self.compute_signature(k)}\n{v}'
            for k, v in sequence_stats.most_common()
        ])

    def compute_signature(self, sequence: str):
        C = sequence.count('C')
        G = sequence.count('G')
        T = sequence.count('T')
        A = sequence.count('A')
        total = len(sequence)
        return f'CGAT = [{100 * C / total: .1f},{100 * G / total: .1f},{100 * A / total: .1f},{100 * T / total: .1f}] length={total}'
