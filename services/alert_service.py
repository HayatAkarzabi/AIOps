# Service layer for alerts.
# Currently returns simulated data.

from utils.data_generator import generate_alerts

def get_all_alerts():
    """Returns a list of simulated alerts."""
    return generate_alerts(count=10)

def get_alerts_by_status(status: str):
    """Returns simulated alerts filtered by status (active, acknowledged, resolved)."""
    all_alerts = generate_alerts(count=20)
    return [a for a in all_alerts if a["status"].lower() == status.lower()]
