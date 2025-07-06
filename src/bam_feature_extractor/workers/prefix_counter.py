from collections import Counter

from pysam import AlignmentFile

from bam_feature_extractor.core.report import Report
from bam_feature_extractor.core.worker import Worker


class PrefixCounter(Worker):
    description = """
    For each sequence (read), extract a prefix of length N.
    Return a list of (prefix, count) where count is the number of sequence starting with 'prefix'.
    
    Example:
    TTAC: 189
    ATTG: 155
    TTGT: 105
    AAGT: 96
    TAGT: 77
    AGTG: 66
    
    """

    def build_report(self, data: AlignmentFile, report: Report):
        stats = Counter()
        for _ in data.fetch():
            prefix = _.query_sequence[:4]
            stats[prefix] += 1

        report.features['prefix_count'] = '\n'.join([
            f'{k}: {v}'
            for k, v in stats.most_common()
        ])
