# Service layer for anomaly detection results.
# Currently returns simulated data.

from utils.data_generator import generate_anomalies

def get_all_anomalies():
    """Returns a list of simulated detected anomalies."""
    return generate_anomalies(count=15)

def get_anomalies_by_severity(severity: str):
    """Returns simulated anomalies filtered by severity level."""
    all_anomalies = generate_anomalies(count=30)
    return [a for a in all_anomalies if a["severity"].lower() == severity.lower()]
