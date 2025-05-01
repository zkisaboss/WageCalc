import json
import requests

API_KEY = "0344b67881ec4d09ba1c222e1c262309"
API_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
HEADERS = {'Content-type': 'application/json'}
ITEMS = {
    'APU0000702111': 'Bread',
    'APU0000703111': 'Ground Beef',
    'APU0000708111': 'Eggs',
    'APU0000709112': 'Milk'
}

def fetch_bls_data() -> dict:
    payload = json.dumps({
        "seriesid": list(ITEMS.keys()),
        "registrationKey": API_KEY
    })
    response = requests.post(API_URL, data=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def process_bls_data(bls_data, wage=20) -> list:
    results = []
    for series in bls_data.get("Results", {}).get("series", []):
        item = ITEMS.get(series["seriesID"], "Unknown")
        data = series.get("data", [])
        if not data:
            continue

        latest = max(data, key=lambda d: (int(d["year"]), int(d["period"][1:])))
        try:
            price = float(latest["value"].replace(",", ""))
        except ValueError:
            continue

        hourly_units = wage / price
        weekly_units_pt = hourly_units * 16
        weekly_units_ft = hourly_units * 40

        results.append({
            'item': item,
            'price': price,
            'hourly_units': hourly_units,
            'weekly_units_pt': weekly_units_pt,
            'weekly_units_ft': weekly_units_ft
        })
    return results
