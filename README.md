# bam-feature-extractor

Read BAM files in a directory and extract custom features (stored as "reports" in an output directory)

## Features

Some workers (feature extractor) are described in the 'data/reports/' directory.
Each '<feature>.txt' file explains the expected output of a specific feature extractor.

## Install / requirements

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- (Optional?) Install [samtools](https://github.com/samtools)
- Create the python virtual env

```bash
uv sync
```

## Running the program

- put all .bam files in the 'resources/data' directory
- put (or generate) the corresponding .bai index files

```bash
(cd resources/data && samtools index -M *.bam)
```

- run the program

```bash
uv run src/bam_feature_extractor/runner.py
```

- Read all the reports in 'resources/reports'

## Adding custom features

Create a new Worker class and implement the Report generation function.
Examples are available in the 'src/bam_feature_extractor/workers' directory.

Add your worker in the list of workings in 'runner.py'. 

```python
def main():
    batch = Batch([
        PrefixCounter(),
        AlignementRatio(),
        SequenceExtractor(),
        PosCounter(),
        YourCustomWorker(), # <------ Your worker goes here !
    ])
    batch.execute(input_dir=INPUT_PATH, output_dir=ROOT_PATH / 'reports')

```
