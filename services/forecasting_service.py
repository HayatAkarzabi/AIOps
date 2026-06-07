# Service layer for forecast predictions.
# Currently returns simulated data.

from utils.data_generator import generate_forecasts

def get_all_forecasts():
    """Returns a list of simulated forecast data points."""
    return generate_forecasts(count=15)
