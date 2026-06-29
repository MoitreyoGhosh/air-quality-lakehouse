"""
Lakehouse Dataset Validator
"""

from pathlib import Path
import duckdb
import pandas as pd

from src.lakehouse.metadata import (
    register_validation,
    register_statistics
)


class DatasetValidator:

    def __init__(self, dataset_path: Path, layer: str = ""):

        self.dataset_path = Path(dataset_path)

        self.dataset_name = self.dataset_path.stem

        self.layer = layer

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
                f"Unsupported format: {suffix}"
            )

    # =====================================================
    # Basic Checks
    # =====================================================

    def file_exists(self):

        return self.dataset_path.exists()

    def row_count(self):

        return len(self.df)

    def column_count(self):

        return len(self.df.columns)

    def is_empty(self):

        return self.df.empty

    def duplicate_rows(self):

        return int(self.df.duplicated().sum())

    def missing_values(self):

        return int(self.df.isnull().sum().sum())

    # =====================================================
    # Dataset Statistics
    # =====================================================

    def calculate_statistics(self):

        return {

            "row_count": self.row_count(),

            "column_count": self.column_count(),

            "null_count": self.missing_values(),

            "duplicate_count": self.duplicate_rows()

        }

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
    # Environmental Validation
    # (Will be expanded later)
    # =====================================================

    def validate_aqi_range(self):

        if "aqi" not in self.df.columns:
            return True

        return self.df["aqi"].between(0, 500).all()

    def validate_pm25(self):

        if "pm25" not in self.df.columns:
            return True

        return (self.df["pm25"] >= 0).all()

    def validate_pm10(self):

        if "pm10" not in self.df.columns:
            return True

        return (self.df["pm10"] >= 0).all()

    def validate_primary_key(self):

        if "station_id" not in self.df.columns:
            return True

        if "datetime" not in self.df.columns:
            return True

        return not self.df.duplicated(
            subset=["station_id", "datetime"]
        ).any()

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

            "empty": self.is_empty(),

            "aqi_range": self.validate_aqi_range(),

            "pm25_range": self.validate_pm25(),

            "pm10_range": self.validate_pm10(),

            "primary_key": self.validate_primary_key()

        }

        if expected_columns:

            report["schema"] = self.validate_schema(
                expected_columns
            )

        # -------------------------------------------------
        # Store Dataset Statistics
        # -------------------------------------------------

        stats = self.calculate_statistics()

        register_statistics(

            dataset_name=self.dataset_name,

            row_count=stats["row_count"],

            column_count=stats["column_count"],

            null_count=stats["null_count"],

            duplicate_count=stats["duplicate_count"]

        )

        # -------------------------------------------------
        # Store Validation Results
        # -------------------------------------------------

        for key, value in report.items():

            if key == "schema":

                status = "PASS" if value["passed"] else "FAIL"

                register_validation(

                    dataset_name=self.dataset_name,

                    layer=self.layer,

                    check_name="schema",

                    status=status,

                    value=f"{len(value['actual'])} columns"

                )

            else:

                if isinstance(value, bool):

                    status = "PASS" if value else "FAIL"

                else:

                    status = "PASS"

                register_validation(

                    dataset_name=self.dataset_name,

                    layer=self.layer,

                    check_name=key,

                    status=status,

                    value=str(value)

                )

        return report

    # =====================================================
    # Print Validation Report
    # =====================================================

    def print_report(self, report):

        print("=" * 60)
        print(f"Validation Report : {self.dataset_name}")
        print("=" * 60)

        print(f"File Exists      : {report['file_exists']}")
        print(f"Rows             : {report['rows']}")
        print(f"Columns          : {report['columns']}")
        print(f"Duplicates       : {report['duplicates']}")
        print(f"Missing Values   : {report['missing_values']}")
        print(f"Empty Dataset    : {report['empty']}")
        print(f"AQI Range        : {report['aqi_range']}")
        print(f"PM2.5 Range      : {report['pm25_range']}")
        print(f"PM10 Range       : {report['pm10_range']}")
        print(f"Primary Key      : {report['primary_key']}")

        if "schema" in report:

            schema = report["schema"]

            print()
            print("Schema Validation")
            print("--------------------------")
            print(f"Expected Columns : {len(schema['expected'])}")
            print(f"Actual Columns   : {len(schema['actual'])}")
            print(f"PASS             : {schema['passed']}")

        print("=" * 60)