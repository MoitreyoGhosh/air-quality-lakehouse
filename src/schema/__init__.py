"""
Environmental Intelligence Framework
====================================

Schema Package

The schema layer standardizes datasets from different
sources into a common schema before they enter the
Lakehouse.

Responsibilities
----------------
- Column mapping
- Schema registration
- Schema lookup
- Schema standardization

This package is intentionally independent of any
specific data source.

Workflow
--------
Connector
    ↓
Schema Mapper
    ↓
Ingestion
    ↓
Bronze Layer
"""

from .registry import SchemaRegistry

__all__ = [
    "SchemaRegistry",
]