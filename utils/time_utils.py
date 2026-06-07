# Time-related utility functions.
# Helps with consistent timestamp formatting across the project.

from datetime import datetime, timedelta
from typing import Union

def now_iso() -> str:
    """Returns the current UTC time as an ISO 8601 string."""
    return datetime.utcnow().isoformat() + "Z"

def hours_ago(hours: Union[int, float]) -> str:
    """Returns an ISO timestamp for 'hours' ago from now."""
    return (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"

def parse_iso(iso_string: str) -> datetime:
    """Parses an ISO 8601 string back into a datetime object."""
    # Remove trailing 'Z' and parse
    return datetime.fromisoformat(iso_string.replace("Z", "+00:00"))

def format_timestamp(dt: datetime) -> str:
    """Formats a datetime object into a human-readable string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")
