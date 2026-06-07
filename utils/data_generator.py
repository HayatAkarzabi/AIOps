# Utility to generate realistic time-series metrics data for ML testing.
# Run directly: python utils/data_generator.py

import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

SEED = 42
ANOMALY_TYPES = ["cpu_spike", "latency_spike", "error_spike",
                 "transaction_drop", "failed_transaction_spike"]


def _compute_seasonal_factor(hours: np.ndarray) -> np.ndarray:
    """Compute a daily pattern multiplier for each hour.

    Returns values near 1.0 during peak hours (2 PM) and ~0.3 at night.
    """
    factor = np.full_like(hours, 0.3, dtype=float)
    mask = (hours >= 6) & (hours <= 22)
    factor[mask] = 0.3 + 0.7 * np.sin(np.pi * (hours[mask] - 6) / 16)
    return factor


def _generate_base_series(n: int, timestamps: pd.DatetimeIndex) -> pd.DataFrame:
    """Create a DataFrame of realistic base metrics with seasonality and trends."""
    np.random.seed(SEED)

    hours = timestamps.hour
    seasonal = _compute_seasonal_factor(hours)

    # Lower activity on weekends
    weekend = np.where(timestamps.dayofweek >= 5, 0.6, 1.0)

    # Slight upward trend over the full period
    trend = np.linspace(0.95, 1.05, n)

    cpu = np.clip((30 + 30 * seasonal) * weekend * trend + np.random.normal(0, 3, n), 10, 95)
    memory = np.clip((35 + 20 * seasonal) * weekend + np.random.normal(0, 2, n), 20, 95)
    latency = np.clip((100 + 200 * seasonal) * weekend * trend + np.random.normal(0, 30, n), 50, 2000)
    error_rate = np.clip((1 + 3 * seasonal) * weekend + np.random.exponential(1, n), 0, 15)
    connections = np.clip((300 + 800 * seasonal) * weekend * trend + np.random.normal(0, 100, n), 50, 5000)
    tx_count = np.clip((500 + 1000 * seasonal) * weekend * trend + np.random.normal(0, 100, n), 100, 3000)

    # failed_transactions derived from transaction_count and error_rate_percent
    failed = (tx_count * error_rate / 100) + np.random.poisson(3, n)
    failed = np.clip(failed, 0, tx_count // 2)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "cpu_usage_percent": cpu.round(2),
        "memory_usage_percent": memory.round(2),
        "request_latency_ms": latency.round(2),
        "error_rate_percent": error_rate.round(2),
        "active_connections": connections.round(0).astype(int),
        "transaction_count": tx_count.round(0).astype(int),
        "failed_transactions": failed.round(0).astype(int),
    })
    return df


def _inject_anomalies(df: pd.DataFrame, ratio: float) -> pd.DataFrame:
    """Randomly inject anomalies into a copy of the DataFrame."""
    df = df.copy()
    n = len(df)
    df["is_anomaly"] = 0
    df["anomaly_type"] = "normal"

    count = int(n * ratio)
    indices = np.random.choice(n, count, replace=False)

    for idx in indices:
        atype = np.random.choice(ANOMALY_TYPES)
        df.at[idx, "is_anomaly"] = 1
        df.at[idx, "anomaly_type"] = atype

        if atype == "cpu_spike":
            df.at[idx, "cpu_usage_percent"] = round(np.random.uniform(85, 100), 2)

        elif atype == "latency_spike":
            df.at[idx, "request_latency_ms"] = round(np.random.uniform(1500, 5000), 2)

        elif atype == "error_spike":
            df.at[idx, "error_rate_percent"] = round(np.random.uniform(30, 95), 2)
            # Also bump failed transactions proportionally
            tx = df.at[idx, "transaction_count"]
            df.at[idx, "failed_transactions"] = int(tx * df.at[idx, "error_rate_percent"] / 100)

        elif atype == "transaction_drop":
            original = df.at[idx, "transaction_count"]
            df.at[idx, "transaction_count"] = max(1, int(original / np.random.uniform(5, 20)))

        elif atype == "failed_transaction_spike":
            tx = df.at[idx, "transaction_count"]
            df.at[idx, "failed_transactions"] = int(tx * np.random.uniform(0.3, 0.8))

    return df


def generate_metrics_dataset(
    days: int = 7,
    freq: str = "5min",
    anomaly_ratio: float = 0.03,
    save_path: str = "data/raw/metrics.csv",
) -> pd.DataFrame:
    """Generate realistic time-series metrics with injected anomalies.

    Parameters
    ----------
    days : int
        Number of days of historical data.
    freq : str
        Pandas frequency string (default "5min").
    anomaly_ratio : float
        Fraction of rows to mark as anomalous (0 to 1).
    save_path : str
        File path for the output CSV.

    Returns
    -------
    pd.DataFrame
        Generated dataset with columns:
        timestamp, cpu_usage_percent, memory_usage_percent,
        request_latency_ms, error_rate_percent, active_connections,
        transaction_count, failed_transactions, is_anomaly, anomaly_type
    """
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    timestamps = pd.date_range(start=start, end=end, freq=freq)

    df = _generate_base_series(len(timestamps), timestamps)
    df = _inject_anomalies(df, anomaly_ratio)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    df.to_csv(save_path, index=False)

    return df


if __name__ == "__main__":
    df = generate_metrics_dataset()
    anomaly_count = df["is_anomaly"].sum()
    print(f"Rows generated: {len(df)}")
    print(f"Anomalies injected: {anomaly_count} ({anomaly_count / len(df) * 100:.2f}%)")
    print(f"Saved to: data/raw/metrics.csv")
