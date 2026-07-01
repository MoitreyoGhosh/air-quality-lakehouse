"""
ingestion.py
=====================================

Near Real-Time Open-Meteo Ingestion

Responsibilities
----------------
✓ Load station metadata
✓ Fetch Weather & AQI data
✓ Parse API responses into canonical DataFrames
✓ Return datasets for Bronze ingestion

Not Responsible For
-------------------
✗ Saving files
✗ Bronze Layer
✗ Silver Layer
✗ Validation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import logging
import pandas as pd

from src.realtime.fetcher import OpenMeteoFetcher


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Constants
# ==========================================================

STATION_MASTER = (
    Path("data")
    / "metadata"
    / "station_master.csv"
)


# ==========================================================
# Dataset Containers
# ==========================================================

@dataclass(slots=True)
class StationRealtimeData:
    """
    Realtime datasets for a single station.
    """

    current_weather: pd.DataFrame
    forecast_weather: pd.DataFrame
    current_air_quality: pd.DataFrame
    forecast_air_quality: pd.DataFrame


@dataclass(slots=True)
class RealtimeDatasets:
    """
    Complete realtime ingestion result.
    """

    current_weather: pd.DataFrame
    forecast_weather: pd.DataFrame
    current_air_quality: pd.DataFrame
    forecast_air_quality: pd.DataFrame
    fetched_at: datetime


# ==========================================================
# Realtime Ingestion
# ==========================================================

class RealtimeIngestion:
    """
    Near Real-Time Open-Meteo ingestion pipeline.
    """

    def __init__(
        self,
    ) -> None:

        self.fetcher = OpenMeteoFetcher()

        self.station_master = (
            self._load_station_master()
        )

    # ======================================================
    # Station Metadata
    # ======================================================

    @staticmethod
    def _load_station_master(
    ) -> pd.DataFrame:
        """
        Load station metadata.
        """

        if not STATION_MASTER.exists():

            raise FileNotFoundError(
                f"Station master not found:\n"
                f"{STATION_MASTER.resolve()}"
            )

        stations = pd.read_csv(
            STATION_MASTER
        )

        required = {
            "station_id",
            "station_name",
            "district",
            "latitude",
            "longitude",
        }

        missing = required - set(
            stations.columns
        )

        if missing:
            raise ValueError(
                "Station master missing columns: "
                f"{sorted(missing)}"

            )

        logger.info(
            "Loaded %d monitoring stations.",
            len(stations),

        )

        return stations

    # ======================================================
    # Station Metadata Helper
    # ======================================================

    @staticmethod
    def _add_station_metadata(
        df: pd.DataFrame,
        station: pd.Series,
    ) -> pd.DataFrame:
        """
        Append station metadata to dataframe.
        """

        if df.empty:
            return df

        metadata = {
            "station_id": station["station_id"],
            "station_name": station["station_name"],
            "district": station["district"],
            "latitude": station["latitude"],
            "longitude": station["longitude"],
        }

        for column, value in reversed(
            list(metadata.items())
        ):

            df.insert(
                0,
                column,
                value,
            )

        return df
    
        # ======================================================
    # Current Weather Parser
    # ======================================================

    def _parse_current_weather(
        self,
        payload: dict[str, Any],
        station: pd.Series,
    ) -> pd.DataFrame:
        """
        Parse current weather response.
        """

        current = payload.get("current")

        if current is None:

            logger.warning(
                "[%s] Missing current weather.",
                station["station_name"],
            )

            return pd.DataFrame()

        df = pd.DataFrame([current])

        df = self._add_station_metadata(
            df,
            station,
        )

        return df

    # ======================================================
    # Forecast Weather Parser
    # ======================================================

    def _parse_forecast_weather(
        self,
        payload: dict[str, Any],
        station: pd.Series,
    ) -> pd.DataFrame:
        """
        Parse hourly weather forecast.
        """

        hourly = payload.get("hourly")

        if hourly is None:

            logger.warning(
                "[%s] Missing weather forecast.",
                station["station_name"],
            )

            return pd.DataFrame()

        df = pd.DataFrame(hourly)

        df = self._add_station_metadata(
            df,
            station,
        )

        return df

    # ======================================================
    # Current AQI Parser
    # ======================================================

    def _parse_current_air_quality(
        self,
        payload: dict[str, Any],
        station: pd.Series,
    ) -> pd.DataFrame:
        """
        Parse current air-quality response.
        """

        current = payload.get("current")

        if current is None:

            logger.warning(
                "[%s] Missing current AQI.",
                station["station_name"],
            )

            return pd.DataFrame()

        df = pd.DataFrame([current])

        df = self._add_station_metadata(
            df,
            station,
        )

        return df

    # ======================================================
    # Forecast AQI Parser
    # ======================================================

    def _parse_forecast_air_quality(
        self,
        payload: dict[str, Any],
        station: pd.Series,
    ) -> pd.DataFrame:
        """
        Parse hourly air-quality forecast.
        """

        hourly = payload.get("hourly")

        if hourly is None:

            logger.warning(
                "[%s] Missing AQI forecast.",
                station["station_name"],
            )

            return pd.DataFrame()

        df = pd.DataFrame(hourly)

        df = self._add_station_metadata(
            df,
            station,
        )

        return df
    
        # ======================================================
    # Fetch One Station
    # ======================================================

    def fetch_station(
        self,
        station: pd.Series,
    ) -> StationRealtimeData:
        """
        Fetch realtime weather and air quality for one station.
        """

        station_id = station["station_id"]

        station_name = station["station_name"]

        latitude = float(
            station["latitude"]
        )

        longitude = float(
            station["longitude"]
        )

        logger.info(
            "Fetching station [%s - %s]",
            station_id,
            station_name,
        )

        # --------------------------------------------------
        # Fetch Weather
        # --------------------------------------------------

        weather_response = self.fetcher.fetch_weather(
            station_id=station_id,
            latitude=latitude,
            longitude=longitude,
        )

        # --------------------------------------------------
        # Fetch Air Quality
        # --------------------------------------------------

        air_response = self.fetcher.fetch_air_quality(
            station_id=station_id,
            latitude=latitude,
            longitude=longitude,
        )

        # --------------------------------------------------
        # Parse Weather
        # --------------------------------------------------

        if weather_response.success:
            current_weather = self._parse_current_weather(
                weather_response.payload or {},
                station,
            )

            forecast_weather = self._parse_forecast_weather(
                weather_response.payload or {},
                station,
            )

        else:
            logger.warning(
                "[%s - %s] Weather request failed: %s",
                station_id,
                station_name,
                weather_response.error,
            )

            current_weather = pd.DataFrame()
            forecast_weather = pd.DataFrame()

        # --------------------------------------------------
        # Parse AQI
        # --------------------------------------------------

        if air_response.success:
            current_air_quality = self._parse_current_air_quality(
                air_response.payload or {},
                station,
            )

            forecast_air_quality = self._parse_forecast_air_quality(
                air_response.payload or {},
                station,
            )

        else:
            logger.warning(
                "[%s - %s] AQI request failed: %s",
                station_id,
                station_name,
                air_response.error,
            )

            current_air_quality = pd.DataFrame()
            forecast_air_quality = pd.DataFrame()

        logger.info(
            "Completed station [%s - %s]",
            station_id,
            station_name,

        )

        return StationRealtimeData(
            current_weather=current_weather,
            forecast_weather=forecast_weather,
            current_air_quality=current_air_quality,
            forecast_air_quality=forecast_air_quality,
        )

    # ======================================================
    # Fetch All Stations
    # ======================================================

    def fetch_all(
        self,
    ) -> RealtimeDatasets:
        """
        Fetch realtime datasets for all monitoring stations.
        """

        logger.info(
            "Starting realtime ingestion..."
        )

        weather_current = []
        weather_forecast = []
        air_current = []
        air_forecast = []

        for _, station in self.station_master.iterrows():
            result = self.fetch_station(
                station
            )

            if not result.current_weather.empty:
                weather_current.append(
                    result.current_weather
                )

            if not result.forecast_weather.empty:
                weather_forecast.append(
                    result.forecast_weather
                )

            if not result.current_air_quality.empty:
                air_current.append(
                    result.current_air_quality
                )

            if not result.forecast_air_quality.empty:
                air_forecast.append(
                    result.forecast_air_quality
                )

        datasets = RealtimeDatasets(
            current_weather=(
                pd.concat(
                    weather_current,
                    ignore_index=True,
                )
                if weather_current
                else pd.DataFrame()
            ),

            forecast_weather=(
                pd.concat(
                    weather_forecast,
                    ignore_index=True,
                )
                if weather_forecast
                else pd.DataFrame()
            ),

            current_air_quality=(
                pd.concat(
                    air_current,
                    ignore_index=True,
                )

                if air_current
                else pd.DataFrame()
            ),

            forecast_air_quality=(
                pd.concat(
                    air_forecast,
                    ignore_index=True,
                )

                if air_forecast
                else pd.DataFrame()
            ),

            fetched_at=datetime.now(),
        )

        logger.info(
            "Realtime ingestion completed."
        )
        logger.info(
            "Current Weather : %d rows",
            len(datasets.current_weather),
        )
        logger.info(
            "Forecast Weather : %d rows",
            len(datasets.forecast_weather),
        )
        logger.info(
            "Current AQI : %d rows",
            len(datasets.current_air_quality),
        )
        logger.info(
            "Forecast AQI : %d rows",
            len(datasets.forecast_air_quality),
        )

        return datasets

    # ======================================================
    # Cleanup
    # ======================================================

    def close(
        self,
    ) -> None:
        """
        Close Open-Meteo HTTP session.
        """
        self.fetcher.close()

        logger.info(
            "Realtime ingestion closed."
        )