"""
database
=====================================

Database Infrastructure

Provides the core DuckDB functionality for the
Environmental Intelligence Lakehouse.
"""

from .connection import database
from .initializer import initializer
from .utils import DatabaseUtils

__all__ = [
    "database",
    "initializer",
    "DatabaseUtils",
]