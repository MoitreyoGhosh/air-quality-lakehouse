"""
demo.py

Demonstration of the Analytics Module.

This script validates:

1. DuckDB connection
2. AnalyticsEngine
3. SQL Queries
4. Plotting utilities
"""

from src.analytics.analytics import AnalyticsEngine
from src.analytics.plots import Plotter


def main():

    engine = AnalyticsEngine()

    print("=" * 70)
    print("ENVIRONMENTAL ANALYTICS DEMO")
    print("=" * 70)

    # --------------------------------------------------
    print("\nLoading Daily AQI...")
    daily_aqi = engine.daily_aqi()
    print(daily_aqi.head())

    Plotter.aqi_trend(daily_aqi)

    # --------------------------------------------------
    print("\nLoading Daily PM2.5...")
    pm25 = engine.daily_pm25()
    print(pm25.head())

    Plotter.pm25_trend(pm25)

    # --------------------------------------------------
    print("\nLoading Daily PM10...")
    pm10 = engine.daily_pm10()
    print(pm10.head())

    Plotter.pm10_trend(pm10)

    # --------------------------------------------------
    print("\nLoading Station Summary...")
    stations = engine.average_aqi_by_station()
    print(stations.head())

    Plotter.station_comparison(stations)

    # --------------------------------------------------
    print("\nLoading Correlation Dataset...")
    corr = engine.aqi_weather()

    Plotter.correlation_heatmap(corr)

    engine.close()

    print("\nDemo completed successfully.")


if __name__ == "__main__":
    main()