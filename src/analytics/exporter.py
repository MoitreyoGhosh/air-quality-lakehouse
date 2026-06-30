"""
exporter.py

Export Analytics Results.

Supported Formats
-----------------
1. CSV
2. Excel
"""

from pathlib import Path

from src.analytics.analytics import AnalyticsEngine


class AnalyticsExporter:

    def __init__(self):

        self.engine = AnalyticsEngine()

        self.output_dir = Path("reports")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # Generic Export
    # =====================================================

    def export_dataframe(
        self,
        dataframe,
        filename
    ):

        csv_path = self.output_dir / f"{filename}.csv"
        excel_path = self.output_dir / f"{filename}.xlsx"

        dataframe.to_csv(
            csv_path,
            index=False
        )

        dataframe.to_excel(
            excel_path,
            index=False
        )

        print(f"Saved {csv_path}")
        print(f"Saved {excel_path}")

    # =====================================================
    # Export Reports
    # =====================================================

    def export_average_aqi(self):

        df = self.engine.average_aqi_by_station()

        self.export_dataframe(
            df,
            "average_aqi_by_station"
        )

    def export_daily_aqi(self):

        df = self.engine.daily_aqi()

        self.export_dataframe(
            df,
            "daily_aqi"
        )

    def export_pm25(self):

        df = self.engine.daily_pm25()

        self.export_dataframe(
            df,
            "daily_pm25"
        )

    def export_pm10(self):

        df = self.engine.daily_pm10()

        self.export_dataframe(
            df,
            "daily_pm10"
        )

    def export_weather(self):

        df = self.engine.temperature_trend()

        self.export_dataframe(
            df,
            "temperature_trend"
        )

    # =====================================================

    def export_all(self):

        self.export_average_aqi()

        self.export_daily_aqi()

        self.export_pm25()

        self.export_pm10()

        self.export_weather()

    # =====================================================

    def close(self):

        self.engine.close()


if __name__ == "__main__":

    exporter = AnalyticsExporter()

    exporter.export_all()

    exporter.close()