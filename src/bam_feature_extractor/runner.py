from pathlib import Path

from easy_kit.timing import setup_timing

from bam_feature_extractor.core.batch import Batch
from bam_feature_extractor.workers.generic_metadata import GenericMetadata
from bam_feature_extractor.workers.read_stats import ReadsStats
from bam_feature_extractor.workers.region_stats import RegionStats

ROOT_PATH = Path.cwd() / 'resources'
INPUT_PATH = ROOT_PATH / 'data'


def main():
    batch = Batch([
        # PrefixCounter(),
        # AlignementRatio(),
        # SequenceExtractor(),
        # PosCounter(),
        GenericMetadata(),
        RegionStats(),
        ReadsStats(),
    ])
    batch.execute(input_dir=INPUT_PATH, output_dir=ROOT_PATH / 'reports')


if __name__ == '__main__':
    setup_timing()
    main()
