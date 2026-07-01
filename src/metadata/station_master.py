"""
station_master.py
=====================================

Builds the canonical Station Master.

Source:
    data/metadata/station_metadata_v1.csv

Output:
    data/metadata/station_master.csv
"""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
METADATA_FILE = ROOT / "data" / "metadata" / "station_metadata_v1.csv"
WBPCB_DIR = ROOT / "data" / "raw" / "wbpcb"
OPENMETEO_DIR = ROOT / "data" / "raw" / "open-meteo-weather"
OUTPUT_FILE = ROOT / "data" / "metadata" / "station_master.csv"


class StationMaster:

    def __init__(self):

        self.metadata = pd.read_csv(METADATA_FILE)

    @staticmethod
    def normalize(text: str) -> str:
        return (
            str(text)
            .lower()
            .replace(",", "")
            .replace(".", "")
            .replace("-", " ")
            .replace("_", " ")
            .strip()
        )

    def build(self):

        df = self.metadata.copy()

        # ---------------------------------------------------
        # WBPCB datasets
        # ---------------------------------------------------

        wbpcb_lookup = {}

        for file in WBPCB_DIR.glob("*.xlsx"):

            dataset = file.stem
            station = dataset.split("-Jan")[0].strip()
            wbpcb_lookup[self.normalize(station)] = dataset

        # ---------------------------------------------------
        # Open-Meteo datasets
        # ---------------------------------------------------

        openmeteo_lookup = {}

        for file in OPENMETEO_DIR.glob("*.xlsx"):

            dataset = file.stem

            station = dataset.split("m_", 1)[1].strip()

            openmeteo_lookup[self.normalize(station)] = dataset

        # ---------------------------------------------------
        # Build mapping
        # ---------------------------------------------------

        records = []

        for _, row in df.iterrows():

            station = row["station_name"]

            key = self.normalize(station)

            records.append(
                {
                    "station_id": row["station_id"],

                    "station_name": station,

                    "wbpcb_station": station,

                    "openmeteo_station": station,

                    "wbpcb_dataset": wbpcb_lookup.get(key),

                    "openmeteo_dataset": openmeteo_lookup.get(key),

                    "location": row["location"],

                    "district": row["district"],

                    "latitude": row["latitude"],

                    "longitude": row["longitude"],

                    "state": row["state"],

                    "start_date": row["start_date"],

                    "end_date": row["end_date"],

                    "total_records": row["total_records"],

                    "schema_version": row["schema_version"],
                }
            )

        return pd.DataFrame(records)

    def save(self):

        df = self.build()

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(
            OUTPUT_FILE,
            index=False,
        )

        print(f"\nCreated {OUTPUT_FILE}")
        print(f"Rows : {len(df)}")

        print("\nPreview\n")
        print(df.head())

        return df


if __name__ == "__main__":

    StationMaster().save()