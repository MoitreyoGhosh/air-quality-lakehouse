"""
Environmental Intelligence Framework
====================================

Connector package.

Connectors are responsible only for reading data from
different sources and returning standardized pandas
DataFrames.

No transformation, validation, metadata registration,
or lakehouse logic should exist here.

Available connectors can include:

- WBPCB
- Open-Meteo
- CPCB
- CSV
- REST APIs
- Databases

These connectors are consumed by the Ingestion layer.
"""
"""
Connector Package
"""

from .base import BaseConnector
from .registry import registry

# Import connectors so they automatically register
from .wbpcb import WBPCBConnector
from .openmeteo import OpenMeteoConnector

__all__ = [
    "BaseConnector",
    "registry",
    "WBPCBConnector",
    "OpenMeteoConnector",
]