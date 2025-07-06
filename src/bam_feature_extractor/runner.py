from pathlib import Path

from easy_kit.timing import setup_timing

from bam_feature_extractor.core.batch import Batch
from bam_feature_extractor.workers.alignment_ratio import AlignementRatio
from bam_feature_extractor.workers.pos_counter import PosCounter
from bam_feature_extractor.workers.prefix_counter import PrefixCounter
from bam_feature_extractor.workers.sequence_extractor import SequenceExtractor

ROOT_PATH = Path.cwd() / 'resources'
INPUT_PATH = ROOT_PATH / 'data'


def main():
    batch = Batch([
        PrefixCounter(),
        AlignementRatio(),
        SequenceExtractor(),
        PosCounter(),
    ])
    batch.execute(input_dir=INPUT_PATH, output_dir=ROOT_PATH / 'reports')


if __name__ == '__main__':
    setup_timing()
    main()
