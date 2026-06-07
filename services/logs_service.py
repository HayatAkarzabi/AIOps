# Service layer for log entries.
# Currently returns simulated data.

from utils.data_generator import generate_logs

def get_all_logs():
    """Returns a list of simulated log entries."""
    return generate_logs(count=30)

def get_logs_by_level(level: str):
    """Returns simulated logs filtered by severity level."""
    all_logs = generate_logs(count=50)
    return [log for log in all_logs if log["level"].upper() == level.upper()]
