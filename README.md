# STM Metro Status to Home Assistant

STM Metro Status is a Python project for residents of the Montreal region using [Home Assistant](https://www.home-assistant.io/). This script scrapes the STM website to get the real-time status of Montreal's metro lines and updates Home Assistant sensors with the data.

This project is licensed under MIT licence.

---

## Features

- Fetches real-time metro status from [STM's website](https://www.stm.info/en/info/service-updates/metro).
- Updates custom Home Assistant sensors with metro status.
- Can be scheduled to run locally using Task Scheduler, cron jobs, or similar tools.
- **NEW: Home Assistant Add-on support for easy installation and hosting**
- Extensible to support additional metro services.

---

## Installation Options

### Option 1: Home Assistant Add-on (Recommended)

The easiest way to use this project is as a Home Assistant add-on:

#### Prerequisites
- Home Assistant with Supervisor (Home Assistant OS, Supervised, or Container with add-ons)
- Network access to STM website

#### Installation Steps

1. **Add Local Add-on Repository**:
   - Copy the entire project folder to your Home Assistant `/addon_configs/local/` directory
   - Name the folder `stm-metro-status`

2. **Install the Add-on**:
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the **three dots menu** → **Repositories**
   - Look for "STM Metro Status" in Local add-ons
   - Click **Install**

3. **Configure the Add-on**:
   - **Update Interval**: Set how often to check metro status (default: 300 seconds)
   - **Ha Token**: Create a Long-Lived Access Token in Home Assistant:
     - Go to your **Profile** → **Long-Lived Access Tokens** → **Create Token**
     - Copy the token and paste it in the add-on configuration

4. **Start the Add-on**:
   - Click **Start** and check the logs for successful operation
   - The add-on will automatically create these sensors:
     - `sensor.metro_line_1_status` (Green Line)
     - `sensor.metro_line_2_status` (Orange Line)
     - `sensor.metro_line_4_status` (Yellow Line)
     - `sensor.metro_line_5_status` (Blue Line)

#### Add-on Configuration

```yaml
update_interval: 300  # Check interval in seconds (1-3600)
ha_token: ""          # Your Home Assistant Long-Lived Access Token
```

#### Customizing Sensors (Optional)

Add this to your `configuration.yaml` for nicer names and icons:

```yaml
homeassistant:
  customize:
    sensor.metro_line_1_status:
      friendly_name: "Metro Line 1 (Green)"
      icon: mdi:subway
    sensor.metro_line_2_status:
      friendly_name: "Metro Line 2 (Orange)"
      icon: mdi:subway
    sensor.metro_line_4_status:
      friendly_name: "Metro Line 4 (Yellow)"
      icon: mdi:subway
    sensor.metro_line_5_status:
      friendly_name: "Metro Line 5 (Blue)"
      icon: mdi:subway
```

### Option 2: Manual Installation (Advanced Users)

#### Requirements

##### Python

- Install the required Python libraries using `pip`:
```bash
pip install requests beautifulsoup4 python-dotenv
```
- Python version `3.12.8`
    - Check your Python version:
```bash
python --version
```

##### Home Assistant
Make sure you have a working Home Assistant server hosted
- If it is running locally use its `IP address` for the `HA_URL` in the `.env` file.
- If it's running on a different network or in the cloud use its `Domain` for the `HA_URL` in the `.env` file.

#### Installation Steps

##### Step 1:
Clone the Git Repo:
```bash
git clone https://github.com/mattyes/STM-webscrap-for-HomeAssistant.git
cd STM-webscrap-for-HomeAssistant
```

##### Step 2:
Create a `.env` file in the project root:

```
HA_TOKEN=your_long_lived_access_token_here 
HA_URL=your_home_assistant_url_here
```

##### Step 3:
The script will automatically create the sensors when first run. No manual helper creation is needed.

##### Step 4:
Run the `metro_status.py` script to ensure it's working:
```bash
python src/metro_status.py
```

##### Step 5:
Setup the script to run every 5 minutes:

- **Windows**: Use Task Scheduler.
- **Linux/MacOS**: Use a cron job:
```bash
*/5 * * * * /path/to/python /path/to/STM-webscrap-for-HomeAssistant/src/metro_status.py
```

## Usage

### Check the Metro Status Manually
Run the script to scrape metro status:
```bash
python src/metro_status.py
```

### Update a Specific Sensor for Testing
Use `test.py` to manually test updating a Home Assistant sensor:
```bash
python src/test.py
```

## Sensors Created

The script automatically creates these sensors in Home Assistant:

- **sensor.metro_line_1_status**: Green Line status
- **sensor.metro_line_2_status**: Orange Line status
- **sensor.metro_line_4_status**: Yellow Line status
- **sensor.metro_line_5_status**: Blue Line status

Each sensor includes:
- **State**: Current status (e.g., "Normal métro service", "Service interruption")
- **Attributes**: Line name, friendly name, and subway icon
- **Updates**: Every 5 minutes (configurable in add-on)

## Troubleshooting

### Add-on Issues
- **401 Unauthorized**: Check your Long-Lived Access Token
- **Connection errors**: Verify your Home Assistant URL and network connectivity
- **Sensors not updating**: Check add-on logs for errors

### Manual Installation Issues
- **Environment variables**: Ensure `.env` file is in the correct location
- **Python dependencies**: Verify all packages are installed
- **Network access**: Ensure the script can reach both STM website and Home Assistant

## Contributing
Contributions are welcome! Here's how you can help:
- Add support for more metro services or transit systems.
- Improve the Home Assistant add-on functionality.
- Add additional configuration options.

To contribute, fork the repository, make your changes, and submit a pull request.

## Roadmap
- ✅ Add the ability to host the script locally on Home Assistant as an add-on.
- Allow dynamic configuration for additional metro services through a YAML file or the Home Assistant UI.
- Add support for other transit systems (Bus, Train, etc.)
- Implement webhook notifications for service disruptions

## License
This project is licensed under the MIT licence.