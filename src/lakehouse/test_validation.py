# from pathlib import Path

# from src.lakehouse.validation import DatasetValidator

# dataset = Path(
#     "lakehouse/gold/environmental_master.parquet"
# )

# validator = DatasetValidator(dataset)

# report = validator.validate()

# for key, value in report.items():

#     print(f"{key} : {value}")

from pathlib import Path

from src.lakehouse.validation import DatasetValidator
from src.database.schema_registry import SCHEMAS

dataset = Path("lakehouse/gold/environmental_master.parquet")

validator = DatasetValidator(dataset)

dataset_name = dataset.stem

report = validator.validate(
    expected_columns=SCHEMAS[dataset_name]
)

print(report)