import requests
import time
import json

URL = "https://www.stm.info/en/ajax/etats-du-service?_="

def fetch_metro_status():
    """Fetch the current status of STM Metro lines."""
    try:
        response = requests.get(URL + str(int(time.time())))
        data = json.loads(response.text)['metro']
        statuses = {}
        for line in data:
            statuses[data[line]['name']] = data[line]['data']['text']
        return statuses
    except Exception as e:
        print(f"Error fetching Metro status: {e}")
        return {}