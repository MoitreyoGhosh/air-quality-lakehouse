"""
Connector Registry for the Environmental Intelligence Framework.

The registry maintains all available connectors and provides
a unified interface for retrieving them.

Example
-------
>>> from src.connectors.registry import ConnectorRegistry
>>> from src.connectors.wbpcb import WBPCBConnector
>>>
>>> registry = ConnectorRegistry()
>>> registry.register("wbpcb", WBPCBConnector)
>>>
>>> connector = registry.create(
...     "wbpcb",
...     source="data/raw"
... )
"""

from __future__ import annotations

from typing import Dict, Type

from .base import BaseConnector


class ConnectorRegistry:
    """
    Registry for all available connectors.
    """

    def __init__(self) -> None:
        self._connectors: Dict[str, Type[BaseConnector]] = {}

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        name: str,
        connector: Type[BaseConnector],
    ) -> None:
        """
        Register a connector class.

        Parameters
        ----------
        name : str
            Connector name.

        connector : BaseConnector
            Connector class.
        """

        key = name.lower().strip()

        if not issubclass(connector, BaseConnector):
            raise TypeError(
                f"{connector.__name__} must inherit BaseConnector."
            )

        self._connectors[key] = connector

    # =====================================================
    # Lookup
    # =====================================================

    def get(
        self,
        name: str,
    ) -> Type[BaseConnector]:
        """
        Return a registered connector class.
        """

        key = name.lower().strip()

        if key not in self._connectors:
            raise KeyError(
                f"Connector '{name}' is not registered."
            )

        return self._connectors[key]

    # =====================================================
    # Factory
    # =====================================================

    def create(
        self,
        name: str,
        *args,
        **kwargs,
    ) -> BaseConnector:
        """
        Create a connector instance.

        Example
        -------
        connector = registry.create(
            "wbpcb",
            source="data/raw"
        )
        """

        connector_class = self.get(name)

        return connector_class(*args, **kwargs)

    # =====================================================
    # Utilities
    # =====================================================

    def available(self) -> list[str]:
        """
        Return registered connector names.
        """

        return sorted(self._connectors.keys())

    def unregister(self, name: str) -> None:
        """
        Remove a connector.
        """

        key = name.lower().strip()

        self._connectors.pop(key, None)

    def clear(self) -> None:
        """
        Remove all registered connectors.
        """

        self._connectors.clear()

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._connectors

    def __len__(self) -> int:
        return len(self._connectors)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(connectors={self.available()})"
        )


# ==========================================================
# Global Registry
# ==========================================================

registry = ConnectorRegistry()