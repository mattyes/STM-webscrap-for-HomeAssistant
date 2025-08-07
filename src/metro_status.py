import json
import requests
import os
from dotenv import load_dotenv
import time


load_dotenv()

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

# Configuration
URL = "https://www.stm.info/en/ajax/etats-du-service?_="
LINE_SENSORS = {
    "Line 1 - Green": "sensor.metro_line_1_status",
    "Line 2 - Orange": "sensor.metro_line_2_status",
    "Line 5 - Blue": "sensor.metro_line_5_status",
    "Line 4 - Yellow": "sensor.metro_line_4_status",
}

def scrape_metro_status2():
    try:

        req = requests.get(URL + str(int(time.time())))
        data = json.loads(req.text)['metro']

        statuses = {}

        for metro in data:
            statuses[data[metro]['name']] = data[metro]['data']['text']

        return statuses
    except Exception as e:
        print(f"Error scraping Metro status: {e}")
        return None


def update_home_assistant(lines_status):
    """Updates Home Assistant with the status of each line."""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    for line, data in lines_status.items():
        sensor_id = LINE_SENSORS.get(line)
        if sensor_id:
            print(f"Updating {sensor_id} to {data}")
            payload = {"state": data}
            try:
                response = requests.post(
                    f"{HA_URL}/api/states/{sensor_id}",
                    headers=headers,
                    json=payload,
                )
                if response.status_code == 200:
                    print(f"Successfully updated {sensor_id} to {data}")
                else:
                    print(f"Failed to update {sensor_id}: {response.status_code}, {response.text}")
            except Exception as e:
                print(f"Error updating {sensor_id}: {e}")

if __name__ == "__main__":
    metro_status = scrape_metro_status2()
    if metro_status:
        print("Metro Status:")
        for line, data in metro_status.items():
            print(f"{line}: {data}")
        update_home_assistant(metro_status)