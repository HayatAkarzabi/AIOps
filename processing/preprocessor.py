# Cleans and prepares metrics data for anomaly detection and forecasting.
# Run directly: python processing/preprocessor.py

from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler

REQUIRED_COLUMNS = [
    "timestamp",
    "cpu_usage_percent",
    "memory_usage_percent",
    "request_latency_ms",
    "error_rate_percent",
    "active_connections",
    "transaction_count",
    "failed_transactions",
    "is_anomaly",
    "anomaly_type",
]

FEATURE_COLUMNS = [
    "cpu_usage_percent",
    "memory_usage_percent",
    "request_latency_ms",
    "error_rate_percent",
    "active_connections",
    "transaction_count",
    "failed_transactions",
]


def _validate_df(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def preprocess_metrics_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the metrics DataFrame.

    Steps: copy, convert timestamp, sort, drop duplicates,
           fill missing values, reset index.

    Parameters
    ----------
    df : pd.DataFrame
        Raw metrics data.

    Returns
    -------
    pd.DataFrame
        Cleaned metrics data.
    """
    _validate_df(df)
    result = df.copy()

    result["timestamp"] = pd.to_datetime(result["timestamp"])
    result = result.sort_values("timestamp")

    before = len(result)
    result = result.drop_duplicates()
    if len(result) < before:
        print(f"Removed {before - len(result)} duplicate row(s)")

    numeric_cols = result.select_dtypes(include="number").columns
    result[numeric_cols] = result[numeric_cols].ffill().bfill()

    result["anomaly_type"] = result["anomaly_type"].fillna("normal")
    result["is_anomaly"] = result["is_anomaly"].fillna(0).astype(int)

    result = result.reset_index(drop=True)
    return result


def get_feature_columns() -> list:
    """Return the list of feature column names used for ML models."""
    return FEATURE_COLUMNS.copy()


def prepare_features(df: pd.DataFrame, scale: bool = False):
    """Extract feature columns and optionally scale them.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed metrics data.
    scale : bool
        If True, apply StandardScaler.

    Returns
    -------
    X : pd.DataFrame
        Feature matrix.
    scaler : StandardScaler or None
        Fitted scaler (only returned when scale=True).
    """
    _validate_df(df)
    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    X = df[FEATURE_COLUMNS].copy()

    if scale:
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
        return X_scaled, scaler

    return X


def prepare_forecasting_series(df: pd.DataFrame, metric_name: str) -> pd.DataFrame:
    """Prepare a two-column DataFrame for forecasting a single metric.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed metrics data.
    metric_name : str
        One of the feature columns to forecast.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: timestamp, value
    """
    _validate_df(df)
    if metric_name not in FEATURE_COLUMNS:
        raise ValueError(
            f"Invalid metric '{metric_name}'. Choose from: {FEATURE_COLUMNS}"
        )

    result = df[["timestamp", metric_name]].copy()
    result = result.rename(columns={metric_name: "value"})
    result = result.sort_values("timestamp").reset_index(drop=True)
    return result


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    from ingestion.collector import load_metrics_data

    raw = load_metrics_data()
    print(f"Raw shape: {raw.shape}")

    cleaned = preprocess_metrics_data(raw)
    print(f"Cleaned shape: {cleaned.shape}")

    X = prepare_features(cleaned)
    print(f"Feature shape: {X.shape}")
    print(f"Feature columns: {list(X.columns)}")

    X_scaled, scaler = prepare_features(cleaned, scale=True)
    print(f"\nScaled feature shape: {X_scaled.shape}")
    print(f"Scaler mean: {scaler.mean_}")
    print(f"Scaler std: {scaler.scale_}")

    series = prepare_forecasting_series(cleaned, "cpu_usage_percent")
    print(f"\nForecasting series shape: {series.shape}")
    print(series.head(3).to_string(index=False))
