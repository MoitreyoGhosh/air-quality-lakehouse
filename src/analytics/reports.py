"""
reports.py

Generate analytical reports using the Analytics Engine.
"""

from src.analytics.analytics import AnalyticsEngine


class ReportGenerator:

    def __init__(self):
        self.engine = AnalyticsEngine()

    # =====================================================
    # Metadata Report
    # =====================================================

    def metadata_report(self):

        print("=" * 70)
        print("DATASET SUMMARY")
        print("=" * 70)

        print(self.engine.dataset_count())

        print("\nStations")
        print(self.engine.station_list())

        print("\nDate Range")
        print(self.engine.date_range())

    # =====================================================
    # AQI Report
    # =====================================================

    def aqi_report(self):

        print("=" * 70)
        print("AVERAGE AQI BY STATION")
        print("=" * 70)

        print(
            self.engine.average_aqi_by_station()
        )

    # =====================================================
    # Weather Report
    # =====================================================

    def weather_report(self):

        print("=" * 70)
        print("TEMPERATURE")
        print("=" * 70)

        print(
            self.engine.temperature_trend().head()
        )

        print("=" * 70)
        print("HUMIDITY")
        print("=" * 70)

        print(
            self.engine.humidity_trend().head()
        )

    # =====================================================
    # Full Report
    # =====================================================

    def full_report(self):

        self.metadata_report()

        print()

        self.aqi_report()

        print()

        self.weather_report()

    # =====================================================

    def close(self):
        self.engine.close()


if __name__ == "__main__":

    report = ReportGenerator()

    report.full_report()

    report.close()