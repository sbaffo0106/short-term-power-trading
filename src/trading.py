import pandas as pd


def align_forecast_timestamps(forecast_df):
    """
    Align PVGIS timestamps to hourly market timestamps.
    """
    forecast_df = forecast_df.copy()

    forecast_df["datetime"] = (
        forecast_df["datetime"]
        .dt.floor("h")
    )

    return forecast_df


def merge_market_and_forecast_data(forecast_df, market_df):
    """
    Merge forecast generation data with market prices.
    """
    return pd.merge(
        forecast_df,
        market_df,
        on="datetime",
        how="inner"
    )


def create_day_ahead_position(df):
    """
    Define Day-Ahead traded position equal to forecast generation.
    """
    df = df.copy()

    df["day_ahead_position"] = df["forecast"]

    return df


def calculate_imbalances(df):
    """
    Calculate forecast-driven imbalance volumes.
    """
    df = df.copy()

    df["imbalance"] = (
        df["actual"]
        - df["day_ahead_position"]
    )
    df["absolute_imbalance"] = (
        df["imbalance"]
        .abs()
    )

    return df


def calculate_day_ahead_revenue(df):
    """
    Calculate gross Day-Ahead market revenue.
    """
    df = df.copy()

    df["day_ahead_revenue"] = (
        df["day_ahead_position"]
        * df["price"]
    )

    return df


def run_imbalance_cost_scenarios(df, penalties):
    """
    Estimate imbalance costs and net revenues under multiple penalty scenarios.
    """
    scenario_results = []

    gross_revenue = df["day_ahead_revenue"].sum()

    for scenario, penalty in penalties.items():
        imbalance_cost = (
            df["absolute_imbalance"]
            * df["price"]
            * penalty
        ).sum()

        net_revenue = gross_revenue - imbalance_cost

        scenario_results.append({
            "Scenario": scenario,
            "Gross Revenue (€)": gross_revenue,
            "Estimated Imbalance Cost (€)": imbalance_cost,
            "Estimated Net Revenue (€)": net_revenue
        })

    return pd.DataFrame(scenario_results)