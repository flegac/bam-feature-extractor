from pathlib import Path

from bam_feature_extractor.core.worker import Worker


class Batch:
    def __init__(self, workers: list[Worker]):
        self.workers = workers

    def execute(self, input_dir: Path, output_dir: Path):
        self._execute_by_file(input_dir, output_dir)

    def _execute_by_worker(self, input_dir: Path, output_dir: Path):
        for worker in self.workers:
            worker.write_description(output_dir)
            for path in input_dir.glob('*.bam'):
                worker.execute(path, output_dir)

    def _execute_by_file(self, input_dir: Path, output_dir: Path):
        for path in input_dir.glob('*.bam'):
            for worker in self.workers:
                worker.write_description(output_dir)
                worker.execute(path, output_dir)
