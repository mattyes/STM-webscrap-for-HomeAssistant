# STM Metro Status to Home Assistant

STM Metro Status is a [Home Assistant](https://www.home-assistant.io/) integration to grab the current status of the STM's metro lines. This script uses the STM AJAX API to get the real-time status of Montreal's metro lines and updates Home Assistant sensors with the data.

This project is licensed under MIT licence.

---

## Features

- Fetches real-time metro status from [STM's website](https://www.stm.info/en/info/service-updates/metro).
- Updates custom Home Assistant sensors with metro status.
- Extensible to support additional metro services.

---

There are two ways to install this integration into HomeAssistant you can either install it through HACS or manually.
## Installation (HACS)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mattyes&repository=STM-webscrap-for-HomeAssistant)

You can either click this button or add `mattyes/STM-webscrap-for-HomeAssistant` as a repository in HACS

## Manual Installation

### Step 1:
Clone the Git Repo:
```git clone https://github.com/mattyes/STM-webscrap-for-HomeAssistant.git```

### Step 2:
Copy the repository folder folder into your Home Assistant's `custom_components` directory

### Step 3:
**Restart Home Assistant**

---

## Setup

1. Go to **Settings > Devices & Services**.
2. Click **Add Integration** in the bottom-right corner.
3. Search for **STM Metro Status**.
4. Click it and confirm setup.

---

## Sensors Created

The integration automatically creates the following sensors:

- `sensor.stm_line_1_green`
- `sensor.stm_line_2_orange`
- `sensor.stm_line_5_blue`
- `sensor.stm_line_4_yellow`

Each sensor shows the current status (e.g., "Normal service", "Delays", etc.).

---

## Contributing
Contributions are welcome! Here's how you can help:
- Add support for more metro services or transit systems.

To contribute, fork the repository, make your changes, and submit a pull request.

## Roadmap
- Allow dynamic configuration for additional metro services through a YAML file or the Home Assistant UI.

## Credits
- mattyes - Original script
- jerji - Optimization and addon
- STM - Data (https://www.stm.info/en/ajax/etats-du-service)

## Licence
This project is licensed under the MIT licence.
