"""
fetcher.py
=====================================

Open-Meteo Near Real-Time API Client

Responsibilities
----------------
✓ Fetch Weather (Current + Forecast)
✓ Fetch Air Quality (Current + Forecast)
✓ Return raw JSON responses

Not Responsible For
-------------------
✗ Parsing JSON
✗ DataFrames
✗ Bronze Layer
✗ Silver Layer
✗ Validation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import logging
import requests


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# API Endpoints
# ==========================================================

WEATHER_API = (
    "https://api.open-meteo.com/v1/forecast"
)

AIR_QUALITY_API = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
)


# ==========================================================
# Weather Variables
# ==========================================================

WEATHER_CURRENT = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "precipitation",
    "surface_pressure",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",

]

WEATHER_HOURLY = WEATHER_CURRENT.copy()


# ==========================================================
# Air Quality Variables
# ==========================================================

AQI_CURRENT = [
    "us_aqi",
    "pm2_5",
    "pm10",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "ozone",
    "sulphur_dioxide",
]

AQI_HOURLY = AQI_CURRENT.copy()


# ==========================================================
# Configuration
# ==========================================================

FORECAST_DAYS = 16
AQI_FORECAST_DAYS = 5
TIMEZONE = "Asia/Kolkata"
REQUEST_TIMEOUT = 30


# ==========================================================
# API Response
# ==========================================================

@dataclass(slots=True)
class APIResponse:
    """
    Standard API response.
    """

    success: bool
    endpoint: str
    station_id: str
    payload: dict[str, Any] | None
    error: str | None = None


# ==========================================================
# Open-Meteo Fetcher
# ==========================================================

class OpenMeteoFetcher:
    """
    Open-Meteo REST API Client.
    """

    def __init__(
        self,
        timeout: int = REQUEST_TIMEOUT,
    ) -> None:
        
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "CEIF/1.0",
            "Accept": "application/json",

        })

    # ======================================================
    # Generic Request
    # ======================================================

    def _request(
        self,
        endpoint: str,
        params: dict[str, Any],
        station_id: str,
    ) -> APIResponse:
        """
        Execute a GET request.
        """

        try:
            logger.info(
                "Fetching station %s",
                station_id,
            )

            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return APIResponse(
                success=True,
                endpoint=endpoint,
                station_id=station_id,
                payload=response.json(),
            )

        except Exception as exc:
            logger.exception(
                "Open-Meteo request failed for %s",
                station_id,
            )

            return APIResponse(
                success=False,
                endpoint=endpoint,
                station_id=station_id,
                payload=None,
                error=str(exc),
            )
    

    # ======================================================
    # Weather
    # ======================================================

    def fetch_weather(
        self,
        station_id: str,
        latitude: float,
        longitude: float,
        forecast_days: int = FORECAST_DAYS,
    ) -> APIResponse:
        """
        Fetch current weather and hourly forecast
        in a single API request.
        """

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(
                WEATHER_CURRENT
            ),
            "hourly": ",".join(
                WEATHER_HOURLY
            ),
            "forecast_days": forecast_days,
            "timezone": TIMEZONE,
        }

        return self._request(
            endpoint=WEATHER_API,
            params=params,
            station_id=station_id,
        )

    # ======================================================
    # Air Quality
    # ======================================================

    def fetch_air_quality(
        self,
        station_id: str,
        latitude: float,
        longitude: float,
        forecast_days: int = AQI_FORECAST_DAYS,
    ) -> APIResponse:
        """
        Fetch current air quality and hourly AQI
        forecast in a single API request.
        """

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(
                AQI_CURRENT
            ),
            "hourly": ",".join(
                AQI_HOURLY
            ),
            "forecast_days": forecast_days,
            "timezone": TIMEZONE,
        }

        return self._request(
            endpoint=AIR_QUALITY_API,
            params=params,
            station_id=station_id,
        )

    # ======================================================
    # Health Check
    # ======================================================

    def health_check(
        self,
    ) -> bool:
        """
        Verify Open-Meteo Weather API availability.
        """

        try:
            response = self.session.get(
                WEATHER_API,
                params={
                    "latitude": 22.5726,
                    "longitude": 88.3639,
                    "current": "temperature_2m",
                },
                timeout=10,
            )

            response.raise_for_status()

            logger.info(
                "Open-Meteo API reachable."
            )

            return True

        except Exception:
            logger.exception(
                "Health check failed."
            )

            return False

    # ======================================================
    # Cleanup
    # ======================================================

    def close(
        self,
    ) -> None:
        """
        Close HTTP session.
        """
        self.session.close()

        logger.info(
            "HTTP session closed."
        )
