# test_solar_flare_model.py
from pprint import pprint

from advanced_solar_flare_model import AdvancedSolarFlareModel

# Create the ML predictor
model = AdvancedSolarFlareModel()

# Example mock data (you can swap with real NASA API responses)
recent_flares = [
    {"classType": "M1.2", "beginTime": "2025-11-01T10:00:00Z"},
    {"classType": "C3.4", "beginTime": "2025-11-02T08:00:00Z"}
]
solar_wind = [
    ["2025-11-05T00:00:00Z", 5, 3, -2, 420, 5],
    ["2025-11-05T01:00:00Z", 6, 4, -1, 415, 6]
]
xray_flux = [
    ["2025-11-04T00:00:00Z", 1e-6],
    ["2025-11-04T01:00:00Z", 2e-6],
    ["2025-11-04T02:00:00Z", 3e-6]
]

result = model.predict(recent_flares, solar_wind, xray_flux)
pprint(result)
