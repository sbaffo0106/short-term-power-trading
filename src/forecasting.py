import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def create_time_features(df):
    """
    Add basic time-based forecasting features.
    """
    df = df.copy()

    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month
    df["day_of_year"] = df["datetime"].dt.dayofyear

    return df


def simulate_irradiance_forecast(df, scale=0.10, seed=42):
    """
    Create a synthetic irradiance forecast by adding controlled uncertainty
    to observed irradiance values.
    """
    df = df.copy()

    np.random.seed(seed)

    df["irradiance_forecast"] = (
        df["irradiance"]
        * np.random.normal(
            loc=1.0,
            scale=scale,
            size=len(df)
        )
    )

    df["irradiance_forecast"] = (
        df["irradiance_forecast"]
        .clip(lower=0)
    )

    return df


def chronological_train_test_split(df, split_date, feature_columns, target_column):
    """
    Split dataset chronologically using a date threshold.
    """
    train_mask = df["datetime"] < split_date
    test_mask = df["datetime"] >= split_date

    X = df[feature_columns]
    y = df[target_column]

    X_train = X[train_mask]
    X_test = X[test_mask]
    y_train = y[train_mask]
    y_test = y[test_mask]

    return X_train, X_test, y_train, y_test, train_mask, test_mask


def train_linear_regression(X_train, y_train):
    """
    Train a Linear Regression forecasting model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model


def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    """
    Train a Random Forest forecasting model.
    """
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    return model


def evaluate_forecast(y_true, y_pred):
    """
    Compute standard forecast accuracy metrics.
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(
        mean_squared_error(y_true, y_pred)
    )
    r2 = r2_score(y_true, y_pred)

    return mae, rmse, r2


def build_metrics_table(model_results):
    """
    Build a forecast comparison table.

    model_results should be a list of dictionaries with:
    model, mae, rmse, r2
    """
    return pd.DataFrame({
        "model": [result["model"] for result in model_results],
        "MAE [kW]": [result["mae"] for result in model_results],
        "RMSE [kW]": [result["rmse"] for result in model_results],
        "R²": [result["r2"] for result in model_results]
    })


def get_feature_importance(model, feature_columns):
    """
    Return feature importance table for tree-based models.
    """
    feature_importance = pd.DataFrame({
        "feature": feature_columns,
        "importance": model.feature_importances_
    })

    return feature_importance.sort_values(
        "importance",
        ascending=False
    )