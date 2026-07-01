import zipfile
import tempfile
from pathlib import Path

import pandas as pd


def load_gme_price_sheet(zip_path, hourly_file="Anno 2023_12.xlsx"):
    """
    Load the hourly Day-Ahead price sheet from a GME zip archive.
    """
    with zipfile.ZipFile(zip_path, "r") as z:

        with z.open(hourly_file) as f:

            with tempfile.NamedTemporaryFile(suffix=".xlsx") as tmp:

                tmp.write(f.read())
                tmp.flush()

                prices_df = pd.read_excel(
                    tmp.name,
                    sheet_name="Prezzi-Prices"
                )

    return prices_df


def prepare_market_prices(prices_df):
    """
    Prepare hourly Italian Day-Ahead market prices from the raw GME price sheet.
    """
    market_df = prices_df[
        [
            "   Data/Date\n(YYYYMMDD)",
            "Ora\n/Hour",
            "PUN"
        ]
    ].copy()

    market_df.columns = [
        "date",
        "hour",
        "price"
    ]

    market_df["date"] = pd.to_datetime(
        market_df["date"],
        format="%Y%m%d"
    )

    market_df["hour"] = market_df["hour"] - 1

    market_df["datetime"] = (
        market_df["date"]
        + pd.to_timedelta(market_df["hour"], unit="h")
    )

    market_df = market_df[
        [
            "datetime",
            "price"
        ]
    ]

    return market_df


def load_market_data(file_path):
    """
    Load processed Italian Day-Ahead market prices.
    """
    return pd.read_csv(
        file_path,
        parse_dates=["datetime"]
    )


def load_solar_pvgis_data(file_path):
    """
    Load and clean PVGIS hourly photovoltaic generation data.
    """
    solar_raw = pd.read_csv(
        file_path,
        skiprows=10
    )

    solar_df = solar_raw[
        [
            "time",
            "P",
            "G(i)",
            "H_sun",
            "T2m",
            "WS10m"
        ]
    ].copy()

    solar_df.columns = [
        "datetime",
        "power",
        "irradiance",
        "sun_height",
        "temperature",
        "wind_speed"
    ]

    solar_df = solar_df[
        solar_df["datetime"].str.match(r"^\d{8}:\d{4}$")
    ].copy()

    solar_df["datetime"] = pd.to_datetime(
        solar_df["datetime"],
        format="%Y%m%d:%H%M"
    )

    numeric_columns = [
        "power",
        "irradiance",
        "sun_height",
        "temperature",
        "wind_speed"
    ]

    for col in numeric_columns:
        solar_df[col] = pd.to_numeric(solar_df[col])

    solar_df["power_kw"] = solar_df["power"] / 1000
    solar_df = solar_df[
        [
            "datetime",
            "power",
            "power_kw",
            "irradiance",
            "sun_height",
            "temperature",
            "wind_speed"
        ]
    ]

    return solar_df


def load_forecast_data(file_path):
    """
    Load processed solar generation forecast data.
    """
    return pd.read_csv(
        file_path,
        parse_dates=["datetime"]
    )


def load_trading_results(file_path):
    """
    Load processed Day-Ahead trading results.
    """
    return pd.read_csv(
        file_path,
        parse_dates=["datetime"]
    )