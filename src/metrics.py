import pandas as pd


def quality_report(df):
    """
    Print basic dataframe quality checks.
    """
    print("Rows:", len(df))

    print("\nMissing values:")
    print(df.isna().sum())

    df.info()


def portfolio_performance_table(df):
    """
    Build summary KPI table for portfolio performance analysis.
    """
    total_revenue = df["day_ahead_revenue"].sum()
    average_hourly_revenue = df["day_ahead_revenue"].mean()
    std_hourly_revenue = df["day_ahead_revenue"].std()
    average_absolute_imbalance = df["absolute_imbalance"].mean()
    total_forecast_generation = df["forecast"].sum()
    average_market_price = df["price"].mean()

    performance_df = pd.DataFrame({
        "Metric": [
            "Total Day-Ahead Revenue",
            "Average Hourly Revenue",
            "Hourly Revenue Std. Dev.",
            "Average Absolute Imbalance",
            "Total Forecast Generation",
            "Average Market Price"
        ],
        "Value": [
            f"€{total_revenue:,.2f}",
            f"€{average_hourly_revenue:,.2f}",
            f"€{std_hourly_revenue:,.2f}",
            f"{average_absolute_imbalance:.2f} kW",
            f"{total_forecast_generation:,.0f} kWh",
            f"€{average_market_price:.2f}/MWh"
        ]
    })

    return performance_df