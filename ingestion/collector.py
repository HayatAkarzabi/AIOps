# Reads the simulated metrics dataset and returns a clean Pandas DataFrame.
# Run directly: python ingestion/collector.py

import pandas as pd
import os
from pathlib import Path

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


def load_metrics_data(file_path: str = "data/raw/metrics.csv") -> pd.DataFrame:
    """Read a metrics CSV, validate, sort, and return a clean DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned and sorted metrics data.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If the file is empty or missing required columns.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Metrics file not found: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError(f"Metrics file is empty: {file_path}")

    if "timestamp" not in df.columns:
        raise ValueError("Column 'timestamp' is missing from the dataset")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df


def get_latest_metrics(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Return the latest rows ordered from newest to oldest.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame with a 'timestamp' column.
    limit : int
        Number of rows to return.

    Returns
    -------
    pd.DataFrame
        Latest rows with newest first.
    """
    return df.sort_values("timestamp", ascending=False).head(limit).reset_index(drop=True)


if __name__ == "__main__":
    df = load_metrics_data()
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 5 rows:")
    print(df.head(5).to_string(index=False))
    print(f"\nLatest 5 rows:")
    print(get_latest_metrics(df, limit=5).to_string(index=False))
