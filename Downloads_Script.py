from pathlib import Path
import shutil
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    source_dir: Path
    destination_dir: Path
    dry_run: bool = True

EXTENSION_MAP = {
    'Images': [".jpeg", ".png"],
    'Documents': [".pdf", ".docx", ".exe"],
    'Videos': [".mp4", ".mkv"],
    'Code': [".py", ".html"],
    'Archives': [".zip"]
}

def get_category(file: Path):
    for category, extensions in EXTENSION_MAP.items():
        if file.suffix.lower() in extensions:
            return category
    return "Others"

def organize_files(config: Config):
    print("Scanning:", config.source_dir)

    for file in config.source_dir.iterdir():
        if file.is_file():
            category = get_category(file)
            target_folder = config.destination_dir / category
            target_folder.mkdir(parents=True, exist_ok=True)
            destination = target_folder / file.name

            print("Found:", file.name, "->", category)

            if config.dry_run:
                print(f"[DRY RUN] would move {file.name} -> {target_folder}")
            else:
                shutil.move(str(file), str(destination))
                print(f"Moved {file.name} -> {target_folder}")

if __name__ == "__main__":
    config = Config(
        source_dir=Path.home() / "Downloads",
        destination_dir=Path.home() / "Downloads_Organized",
        dry_run=False
    )

    organize_files(config)