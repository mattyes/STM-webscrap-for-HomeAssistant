# STM Metro Status to Home Assistant

STM Metro Status is a Python project for residents of the Montreal region using [Home Assistant](https://www.home-assistant.io/). This script scrapes the STM website to get the real-time status of Montreal's metro lines and updates Home Assistant sensors with the data.

This project is licensed under [The Unlicense](LICENSE), so feel free to modify and share it as you like.

---

## Features

- Fetches real-time metro status from [STM's website](https://www.stm.info/en/info/service-updates/metro).
- Updates custom Home Assistant sensors with metro status.
- Can be scheduled to run locally using Task Scheduler, cron jobs, or similar tools.
- Extensible to support additional metro services.

---

## Requirements

### Python

- Install the required Python libraries using `pip`:
```pip install requests beautifulsoup4```
- Python version `3.12.8`

### Home Assistant
Make sure you have a working Home Assistant server hosted
- If it is running localy use it's `IP address` for the `HA_URL` in the `.env` file.
- If it's running on a diffrent network or in the cloud use it's `Domain` for the `HA_URL` in the `.env` file.

## Installation
### Step 1:
Clone the Git Repo:
```git clone https://github.com/your-username/STM-Metro-Status.git```

Navigate to the folder:
```cd STM-Metro-Status```

### Step 2:
Create a `.env` file in the project root:

```
HA_TOKEN=your_long_lived_access_token_here 
HA_URL=your_home_assistant_url_here
```
### Step 3:
Create the Home Assistant Helpers:
You need to create **four helpers** in Home Assistant corresponding to the metro lines. These helpers are sensors that will be updated with the metro status:
- sensor.metro_line_1_status
- sensor.metro_line_2_status
- sensor.metro_line_5_status
- sensor.metro_line_4_status

For more information on creating sensors in Home Assistant, refer to the official documentation.

### Step 4:
Run the `metro_status.py` script to ensure it's working:
```python metro_status.py```

### Step 5:
Setup the script to run every 5 minutes:

- **Windows**: Use Task Scheduler.

- **Linux/Macos**: Use a cron job:
`*/5 * * * * /path/to/python /path/to/metro_status.py`

## Usage
### Check the Metro Stage Manually
Run the script to scrape metro status:
`python metro_status.py`
### Update a Specific Sensor for Testing
Use `test.py` to manually test updating a Home Assistant sensor:
`python test.py`

## Contributing
Contributions are welcome! Here's how you can help:
- Add support for more metro services or transit systems.
- Help integrate this project as an add-on for Home Assistant to allow easier hosting.

To contribute, fork the repository, make your changes, and submit a pull request.

## Roadmap
- Add the ability to host the script locally on Home Assistant as an add-on.
- Allow dynamic configuration for additional metro services through a YAML file or the Home Assistant UI.
## Licence
This project is licensed under [The Unlicense](https://unlicense.org/).