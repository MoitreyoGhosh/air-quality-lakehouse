"""
plots.py

Reusable Plotting Module
------------------------

Responsibilities
----------------
1. AQI Trend
2. PM2.5 Trend
3. PM10 Trend
4. Temperature Trend
5. Humidity Trend
6. Station Comparison
7. Correlation Heatmap
8. Generic Time Series Plot

Author:
Environmental Intelligence Lakehouse
"""

from typing import Optional

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ------------------------------------------------------------------
# Plot Style
# ------------------------------------------------------------------

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 11


class Plotter:
    """
    Reusable plotting utilities.
    """

    # ==========================================================
    # Generic Time Series
    # ==========================================================

    @staticmethod
    def timeseries(
        df: pd.DataFrame,
        x: str,
        y: str,
        title: str,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        color: str = "royalblue"
    ):

        plt.figure()

        sns.lineplot(
            data=df,
            x=x,
            y=y,
            color=color,
            linewidth=2
        )

        plt.title(title)

        plt.xlabel(xlabel or x)
        plt.ylabel(ylabel or y)

        plt.tight_layout()
        plt.show()

    # ==========================================================
    # AQI Trend
    # ==========================================================

    @staticmethod
    def aqi_trend(df):

        Plotter.timeseries(
            df=df,
            x="date",
            y="average_aqi",
            title="Average AQI Trend",
            ylabel="AQI",
            color="firebrick"
        )

    # ==========================================================
    # PM2.5 Trend
    # ==========================================================

    @staticmethod
    def pm25_trend(df):

        Plotter.timeseries(
            df=df,
            x="date",
            y="average_pm25",
            title="PM2.5 Trend",
            ylabel="PM2.5",
            color="darkorange"
        )

    # ==========================================================
    # PM10 Trend
    # ==========================================================

    @staticmethod
    def pm10_trend(df):

        Plotter.timeseries(
            df=df,
            x="date",
            y="average_pm10",
            title="PM10 Trend",
            ylabel="PM10",
            color="forestgreen"
        )

    # ==========================================================
    # Temperature Trend
    # ==========================================================

    @staticmethod
    def temperature_trend(df):

        Plotter.timeseries(
            df=df,
            x="date",
            y="average_temperature",
            title="Temperature Trend",
            ylabel="Temperature (°C)",
            color="tomato"
        )

    # ==========================================================
    # Humidity Trend
    # ==========================================================

    @staticmethod
    def humidity_trend(df):

        Plotter.timeseries(
            df=df,
            x="date",
            y="average_humidity",
            title="Humidity Trend",
            ylabel="Humidity (%)",
            color="steelblue"
        )

    # ==========================================================
    # Station Comparison
    # ==========================================================

    @staticmethod
    def station_comparison(
        df: pd.DataFrame,
        x: str = "station_name",
        y: str = "average_aqi"
    ):

        plt.figure(figsize=(14, 6))

        sns.barplot(
            data=df,
            x=x,
            y=y,
            palette="viridis"
        )

        plt.xticks(rotation=90)

        plt.title("Station Comparison")

        plt.tight_layout()

        plt.show()

    # ==========================================================
    # Correlation Heatmap
    # ==========================================================

    @staticmethod
    def correlation_heatmap(df: pd.DataFrame):

        plt.figure(figsize=(10, 8))

        numeric = df.select_dtypes(include="number")

        sns.heatmap(
            numeric.corr(),
            annot=True,
            cmap="coolwarm",
            linewidths=0.5,
            fmt=".2f"
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        plt.show()

    # ==========================================================
    # Histogram
    # ==========================================================

    @staticmethod
    def histogram(
        df: pd.DataFrame,
        column: str,
        bins: int = 30
    ):

        plt.figure()

        sns.histplot(
            df[column],
            bins=bins,
            kde=True,
            color="royalblue"
        )

        plt.title(f"{column} Distribution")

        plt.tight_layout()

        plt.show()

    # ==========================================================
    # Box Plot
    # ==========================================================

    @staticmethod
    def boxplot(
        df: pd.DataFrame,
        column: str
    ):

        plt.figure()

        sns.boxplot(
            y=df[column],
            color="lightgreen"
        )

        plt.title(f"{column} Boxplot")

        plt.tight_layout()

        plt.show()

    # ==========================================================
    # Scatter Plot
    # ==========================================================

    @staticmethod
    def scatter(
        df: pd.DataFrame,
        x: str,
        y: str
    ):

        plt.figure()

        sns.scatterplot(
            data=df,
            x=x,
            y=y
        )

        plt.title(f"{x} vs {y}")

        plt.tight_layout()

        plt.show()