import requests
import os
from dotenv import load_dotenv

load_dotenv()

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

sensor_id = "sensor.metro_line_1_status" # Change this to your sensor id
state = "This sensor is getiing updated!"

data = {"state": state}

response = requests.post(
    f"{HA_URL}/api/states/{sensor_id}",
    headers=headers,
    json=data
)

print(response.status_code, response.json())