# Service layer for metrics data.
# Currently returns simulated data. Replace with real data source later.

from utils.data_generator import generate_metrics

def get_all_metrics():
    """
    Returns a list of simulated system metrics.
    Each metric is a dict with name, value, unit, timestamp, source.
    """
    return generate_metrics(count=20)

def get_metric_by_name(name: str):
    """Returns simulated metrics filtered by name."""
    all_metrics = generate_metrics(count=50)
    return [m for m in all_metrics if m["name"] == name]
