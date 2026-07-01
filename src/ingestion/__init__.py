"""
Environmental Intelligence Framework
====================================

Ingestion Package

The ingestion layer orchestrates data loading from different
connectors into the Lakehouse.

Responsibilities
----------------
- Select the appropriate connector
- Load historical datasets
- Load real-time datasets
- Return standardized DataFrames to the Bronze layer

The ingestion layer does NOT perform:
- Data cleaning
- Feature engineering
- Validation
- Metadata registration
- Analytics
- Forecasting
"""

__all__ = []

# """
# Environmental Intelligence Framework
# ====================================

# Ingestion Package
# """

# from .manager import IngestionManager
# from .historical import HistoricalIngestion
# from .realtime import RealtimeIngestion

# __all__ = [
#     "IngestionManager",
#     "HistoricalIngestion",
#     "RealtimeIngestion",
# ]