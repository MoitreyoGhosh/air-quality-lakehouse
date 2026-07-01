"""
validation
=====================================

Environmental Intelligence Framework

Validation Layer

This package performs quality assessment on canonical
datasets produced by the ingestion pipeline.

Pipeline
--------
Historical Ingestion
        │
        ▼
Validation
        │
        ▼
Bronze Storage

Responsibilities
----------------
✓ Validate canonical schemas
✓ Check data quality
✓ Generate validation reports
✓ Detect anomalies

Not Responsible For
-------------------
✗ Data ingestion
✗ Data cleaning
✗ Feature engineering
✗ Storage
✗ Analytics
"""

from .rules import ValidationRules
from .validator import DataValidator
from .report import ValidationReport

__all__ = [
    "ValidationRules",
    "DataValidator",
    "ValidationReport",
]