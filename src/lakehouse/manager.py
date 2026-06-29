"""
Generic Lakehouse Manager

Responsibilities
----------------
1. Scan source directory
2. Preserve folder hierarchy
3. Copy datasets into Lakehouse
4. Extract metadata
5. Register datasets
6. Register files
7. Log pipeline execution
"""

from pathlib import Path
from datetime import datetime
import shutil

import pandas as pd

from src.lakehouse.metadata import (
    calculate_checksum,
    register_dataset,
    register_file,
    log_pipeline,
)


class LakehouseManager:

    def __init__(
        self,
        source_dir: Path,
        target_dir: Path,
        layer: str
    ):

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.layer = layer.lower()

    # Scan Files
    def scan_files(self):

        supported = []

        for extension in ("*.xlsx", "*.parquet", "*.csv"):
            supported.extend(self.source_dir.rglob(extension))

        return sorted(supported)

    # Preserve Folder Structure
    def copy_dataset(self, source: Path) -> Path:

        relative_path = source.relative_to(self.source_dir)
        destination = self.target_dir / relative_path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(source, destination)
        return destination

    # Dataset Metadata

    def get_dataset_metadata(self, file_path: Path):
        suffix = file_path.suffix.lower()

        try:
            if suffix == ".parquet":
                df = pd.read_parquet(file_path)

            elif suffix == ".xlsx":
                df = pd.read_excel(file_path)

            elif suffix == ".csv":
                df = pd.read_csv(file_path)

            else:
                raise ValueError(
                    f"Unsupported format: {suffix}"
                )

            rows = len(df)
            columns = len(df.columns)

        except Exception:
            # If file cannot be parsed, still register it
            rows = None
            columns = None

        return {

            "rows": rows,
            "columns": columns,
            "size_mb": round(
                file_path.stat().st_size / (1024 * 1024),
                2
            ),
            "checksum": calculate_checksum(file_path)
        }

    # Register Metadata

    def register(self, destination: Path, metadata: dict):
        register_dataset(
            dataset_name=destination.stem,
            layer=self.layer,
            source=str(destination.parent),
            file_format=destination.suffix.replace(".", ""),
            rows=metadata["rows"],
            columns=metadata["columns"],
            version=datetime.now().strftime("%Y%m%d"),
            checksum=metadata["checksum"]
        )

        register_file(
            file_name=destination.name,
            dataset_name=destination.stem,
            layer=self.layer,
            file_path=str(destination),
            file_size_mb=metadata["size_mb"]
        )

    # Main Pipeline
    def ingest(self):
        files = self.scan_files()
        if not files:
            log_pipeline(
                pipeline_name=f"{self.layer.title()} Pipeline",
                layer=self.layer,
                status="FAILED",
                message="No datasets found."
            )
            print("No datasets found.")
            return

        print("=" * 70)
        print(f"{self.layer.upper()} INGESTION")
        print("=" * 70)

        success = 0
        failed = 0

        for source in files:
            try:
                destination = self.copy_dataset(source)
                metadata = self.get_dataset_metadata(destination)
                self.register(destination, metadata)
                success += 1
                print(f"✓ {destination.relative_to(self.target_dir)}")
            except Exception as e:
                failed += 1
                print(f"✗ {source.name}")
                print(e)

        log_pipeline(
            pipeline_name=f"{self.layer.title()} Pipeline",
            layer=self.layer,
            status="SUCCESS" if failed == 0 else "PARTIAL_SUCCESS",
            message=f"{success} succeeded, {failed} failed."
        )

        print()
        print("=" * 70)
        print("Pipeline Summary")
        print("=" * 70)
        print(f"Successful : {success}")
        print(f"Failed     : {failed}")