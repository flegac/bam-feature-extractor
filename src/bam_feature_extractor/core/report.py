from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Report:
    feature: str
    input_file: Path
    features: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def save_at(self, output_dir: Path):
        output_dir = output_dir / self.input_file.stem
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.errors:
            error_file = output_dir / f'{self.input_file.stem}.errors'
            with error_file.open('w') as _:
                _.write('\n'.join(self.errors))

        for name, data in self.features.items():
            file = output_dir / f'{self.input_file.stem}.{name}'
            with file.open('w') as _:
                _.write(data)
