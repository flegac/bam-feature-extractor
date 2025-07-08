from pathlib import Path

from pysam import AlignmentFile

from bam_feature_extractor.core.report import Report
from bam_feature_extractor.core.worker import Worker


class GenericMetadata(Worker):
    description = """
    Extract Metadata from the bam file

    """

    def build_report(self, data: AlignmentFile, report: Report):
        filename = Path(data.filename.decode('utf-8'))
        lines = [
            f'name: {filename.name}',
            f'description: {data.description}',
            f'category: {data.category}',
            f'format: {data.format}',
            f'----- text -----------------------------------',
            f'{data.text.strip()}',
            f'----------------------------------------------',
            '',
            *[
                self.reference_report(data, _) + '\n'
                for _ in data.references
            ],

        ]
        report.features['metadata'] = '\n'.join(lines)

    def reference_report(self, data: AlignmentFile, ref: str):
        reference_length = data.get_reference_length(ref)
        stats = data.get_index_statistics()[data.get_tid(ref)]

        lines = [
            f'[{ref}]',
            f'length: {reference_length}',
            f'reads: {stats.total}',
            f'mapped: {stats.mapped}',
            f'unmapped: {stats.unmapped}',
        ]
        return '\n  '.join(lines)
