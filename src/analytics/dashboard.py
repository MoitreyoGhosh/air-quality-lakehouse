"""
dashboard.py

Simple Analytics Dashboard.
"""

from src.analytics.analytics import AnalyticsEngine


class Dashboard:

    def __init__(self):

        self.engine = AnalyticsEngine()

    # =====================================================

    def show_summary(self):

        print("=" * 70)
        print("ENVIRONMENTAL ANALYTICS DASHBOARD")
        print("=" * 70)

        print("\nDatasets")
        print(self.engine.dataset_count())

        print("\nStations")
        print(self.engine.station_list())

        print("\nDate Range")
        print(self.engine.date_range())

        print("\nAverage AQI")

        print(
            self.engine.average_aqi_by_station().head(10)
        )

    # =====================================================

    def close(self):

        self.engine.close()


if __name__ == "__main__":

    dashboard = Dashboard()

    dashboard.show_summary()

    dashboard.close()