import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

# Configuration
URL = "https://www.stm.info/en/info/service-updates/metro"
LINE_SENSORS = {
    "line_1": "sensor.metro_line_1_status",
    "line_2": "sensor.metro_line_2_status",
    "line_5": "sensor.metro_line_5_status",
    "line_4": "sensor.metro_line_4_status",
}

def scrape_metro_status():
    """Scrapes the Metro status webpage for all lines."""
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data for each metro line
        lines_status = {}
        main_content = soup.find('div', id='main-content')
        sections = main_content.find_all('section', class_='item')

        for section in sections:
            # Extract line number and name
            line_classes = section['class']
            line_id = next((cls for cls in line_classes if 'line-' in cls), None)  # e.g., "line-1"
            if line_id:
                line_id = line_id.replace('-', '_')  # Convert "line-1" to "line_1"
                print(f"Extracted line_id: {line_id}")  # Debugging

            line_name = section.find('h2').text.strip()  # e.g., "Line 1 - Green"
            status = section.find('p').text.strip()  # e.g., "Normal métro service"

            if line_id:
                lines_status[line_id] = {"line_name": line_name, "status": status}

        return lines_status
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
        print(f"Looking up sensor_id for {line}: {sensor_id}")  # Debugging
        if sensor_id:
            # Extract only the status text for the sensor state
            status = data["status"]
            print(f"Updating {sensor_id} to {status}")
            payload = {"state": status}
            try:
                response = requests.post(
                    f"{HA_URL}/api/states/{sensor_id}",
                    headers=headers,
                    json=payload,
                )
                if response.status_code == 200:
                    print(f"Successfully updated {sensor_id} to {status}")
                else:
                    print(f"Failed to update {sensor_id}: {response.status_code}, {response.text}")
            except Exception as e:
                print(f"Error updating {sensor_id}: {e}")

if __name__ == "__main__":
    metro_status = scrape_metro_status()
    if metro_status:
        print("Metro Status:")
        for line, data in metro_status.items():
            print(f"{data['line_name']}: {data['status']}")
        update_home_assistant(metro_status)
