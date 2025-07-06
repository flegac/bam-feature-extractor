from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Report:
    input_file: Path
    features: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def save_at(self, output_dir: Path):
        output_dir = output_dir / self.input_file.stem
        if self.errors:
            error_file = output_dir.with_suffix('.errors')
            with error_file.open('w') as _:
                _.write('\n'.join(self.errors))

        if len(self.features) > 1:
            output_dir = output_dir / self.input_file.stem
        output_dir.parent.mkdir(parents=True, exist_ok=True)

        for name, data in self.features.items():
            file = output_dir.with_suffix(f'.{name}')
            with file.open('w') as _:
                _.write(data)
