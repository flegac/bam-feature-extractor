from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path

import pysam
from easy_kit.timing import timing
from pysam import AlignmentFile

from bam_feature_extractor.core.report import Report


class Worker(ABC):
    description: str = ''

    @abstractmethod
    def build_report(self, data: AlignmentFile, report: Report):
        ...

    def execute(self, input_file: Path, output_dir: Path):
        with sam(path=input_file) as data:
            report = Report(feature=self.__class__.__name__, input_file=input_file)
            with timing(f'{self.__class__.__name__}.execute'):
                self.build_report(data, report)
        report.save_at(output_dir)

    def write_description(self, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        description_path = output_dir / f'{self.__class__.__name__}.txt'
        if not description_path.exists():
            with description_path.open('w') as _:
                _.write(self.description)


@contextmanager
def sam(path: Path):
    data = pysam.AlignmentFile(str(path), "rb")
    yield data
    data.close()
