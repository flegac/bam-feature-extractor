import math

from pysam import AlignmentFile
from tqdm import tqdm

from bam_feature_extractor.core.report import Report
from bam_feature_extractor.core.worker import Worker

# split the reference in regions of equal sizes
REGION_NUMBER = 100


class RegionStats(Worker):
    description = """
    Compute statistics by region (in the reference).
    
    Example:
    [NC_014804.1]
    Number of reads aligned with each region (region_size=20101)
    region.start, region.stop, #reads,
         0,     20101,        532,
     20101,     40202,       2115,
     40202,     60303,       2886,
     60303,     80404,       1859,
     80404,    100505,       2395,
     
    """

    def build_report(self, data: AlignmentFile, report: Report):
        for ref in data.references:
            report.features.update(self.reference_report(data, ref))

    def reference_report(self, data: AlignmentFile, ref: str):
        reference_length = data.get_reference_length(ref)
        stats = data.get_index_statistics()[data.get_tid(ref)]
        reads_number = stats.total
        if reads_number == 0:
            return ''

        region_size = 1 + math.floor(reference_length // REGION_NUMBER)
        regions = [
            (_, _ + region_size)
            for _ in range(0, reference_length, region_size)
        ]
        counts = {
            region: data.count(ref, start=region[0], stop=region[1])
            for region in tqdm(regions)
        }
        counts_by_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
        return {
            'regions': '\n'.join([
                f'[{ref}]',
                f'Number of reads alignment overlaps for each region (region_size={region_size})',
                f'region.start, region.stop, #reads,',
                *[
                    f'{start:10},{stop:10}, {reads:10},'
                    for (start, stop), reads in counts.items()
                ],
            ]),
            'regions_by_count': '\n'.join([
                f'[{ref}]',
                f'Number of reads alignment overlaps for each region (region_size={region_size})',
                f'region.start, region.stop, #reads,',
                *[
                    f'{start:10},{stop:10}, {reads:10},'
                    for (start, stop), reads in counts_by_counts.items()
                ],
            ])
        }
