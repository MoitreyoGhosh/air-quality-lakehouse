"""
validation.py

Lakehouse Dataset Validator
"""

from pathlib import Path

import duckdb
import pandas as pd


class DatasetValidator:

    def __init__(self, dataset_path: Path):

        self.dataset_path = Path(dataset_path)

        self.df = None

    # =====================================================
    # Load Dataset
    # =====================================================

    def load(self):

        suffix = self.dataset_path.suffix.lower()

        if suffix == ".parquet":

            self.df = duckdb.sql(f"""

            SELECT *

            FROM read_parquet('{self.dataset_path}')

            """).df()

        elif suffix == ".csv":

            self.df = pd.read_csv(self.dataset_path)

        elif suffix == ".xlsx":

            self.df = pd.read_excel(self.dataset_path)

        else:

            raise ValueError(
                f"Unsupported format : {suffix}"
            )

    # =====================================================
    # File Exists
    # =====================================================

    def file_exists(self):

        return self.dataset_path.exists()

    # =====================================================
    # Row Count
    # =====================================================

    def row_count(self):

        return len(self.df)

    # =====================================================
    # Column Count
    # =====================================================

    def column_count(self):

        return len(self.df.columns)

    # =====================================================
    # Empty Dataset
    # =====================================================

    def is_empty(self):

        return self.df.empty

    # =====================================================
    # Duplicate Records
    # =====================================================

    def duplicate_rows(self):

        return self.df.duplicated().sum()

    # =====================================================
    # Missing Values
    # =====================================================

    def missing_values(self):

        return self.df.isnull().sum().sum()

    # =====================================================
    # Schema Validation
    # =====================================================

    def validate_schema(self, expected_columns):

        actual_columns = list(self.df.columns)

        return {

            "expected": expected_columns,

            "actual": actual_columns,

            "passed": expected_columns == actual_columns

        }

    # =====================================================
    # Complete Validation
    # =====================================================

    def validate(self, expected_columns=None):

        self.load()

        report = {

            "file_exists": self.file_exists(),

            "rows": self.row_count(),

            "columns": self.column_count(),

            "duplicates": self.duplicate_rows(),

            "missing_values": self.missing_values(),

            "empty": self.is_empty()

        }

        if expected_columns:

            report["schema"] = self.validate_schema(
                expected_columns
            )

        return report

    def print_report(self, report):

        print("=" * 60)
        print("Validation Report")
        print("=" * 60)

        print(f"File Exists     : {report['file_exists']}")
        print(f"Rows            : {report['rows']}")
        print(f"Columns         : {report['columns']}")
        print(f"Duplicates      : {report['duplicates']}")
        print(f"Missing Values  : {report['missing_values']}")
        print(f"Empty Dataset   : {report['empty']}")

        if "schema" in report:

            schema = report["schema"]

            print()

            print("Schema Validation")

            print("-----------------------")

            print(f"Expected Columns : {len(schema['expected'])}")

            print(f"Actual Columns   : {len(schema['actual'])}")

            print(f"PASS             : {schema['passed']}")

        print("=" * 60)