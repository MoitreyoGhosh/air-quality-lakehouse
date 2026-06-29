from src.lakehouse.metadata import (
    list_datasets,
    list_files,
    list_pipeline_runs,
    list_validation_results,
    list_versions,
    list_statistics
)

print("Datasets:", len(list_datasets()))
print("Files:", len(list_files()))
print("Pipeline Runs:", len(list_pipeline_runs()))
print("Validation Results:", len(list_validation_results()))
print("Dataset Versions:", len(list_versions()))
print("Dataset Statistics:", len(list_statistics()))