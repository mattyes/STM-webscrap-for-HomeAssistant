# STM Metro Status → Home Assistant

STM Metro Status is a [Home Assistant](https://www.home-assistant.io/) integration that fetches real-time metro service alerts from the [STM](https://www.stm.info) (Société de transport de Montréal) using their official API.

This project is licensed under MIT licence.

---

## Features

- Fetches real-time metro service alerts from the [STM API](https://api.stm.info/pub/od/i3/v2/messages/etatservice).
- Creates individual sensors for each metro line (Green, Orange, Yellow, Blue).
- Displays "Normal service" when there are no alerts, or the relevant alert description (English, falling back to French).
- Each sensor includes detailed alert information in its attributes.

---

## Prerequisites

You need an **STM API key** to use this integration. Get one from the [STM Developer Portal](https://www.stm.info/a-propos/documents-donnees/donnees-ouvertes).

---

## Installation

### Via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mattyes&repository=STM-webscrap-for-HomeAssistant&category=integration)

Click the button above, or manually add `mattyes/STM-webscrap-for-HomeAssistant` as a custom repository in HACS.

### Manual Installation

```bash
git clone https://github.com/mattyes/STM-webscrap-for-HomeAssistant.git
```

Copy the repository folder into your Home Assistant's `custom_components` directory, then **restart Home Assistant**.

---

## Setup

1. Go to **Settings > Devices & Services**.
2. Click **Add Integration** in the bottom-right corner.
3. Search for **STM Metro Status**.
4. Enter your STM API key when prompted.
5. Click submit.

### Updating your API key

After setup, you can update your API key anytime via **Settings > Devices & Services > STM Metro Status > Configure**.

---

## Sensors Created

The integration creates one sensor per metro line:

| Sensor                    | Line                      |
|---------------------------|---------------------------|
| `sensor.stm_line_1_green`  | Line 1 - Green            |
| `sensor.stm_line_2_orange` | Line 2 - Orange           |
| `sensor.stm_line_4_yellow` | Line 4 - Yellow           |
| `sensor.stm_line_5_blue`   | Line 5 - Blue             |

### State

Each sensor shows the current status, e.g.:
- `"Normal service"` – no alerts for this line
- `"This Saturday, November 14, métro service on line 5 - Blue..."` – service alert description (English preferred, French fallback)

### Attributes

Each sensor includes detailed attributes:

```yaml
line_name: "Line 1 - Green"
has_alerts: true
alert_count: 3
alerts:
  - header: "Your stop"
    description_en: "This stop is cancelled due to roadworks..."
    description_fr: "Cet arrêt est annulé en raison de travaux..."
    route: "1"
  - header: "Your line"
    description_en: "Some stops are cancelled..."
    description_fr: "Certains arrêts sont annulés..."
    route: "1"
```

You can use these attributes in automations or templates.

---

## Automation Examples

### Notify when a line has alerts

```yaml
alias: "STM Metro Alert"
trigger:
  platform: state
  entity_id: sensor.stm_line_5_blue
  not_to: "Normal service"
action:
  service: notify.mobile_app_phone
  data:
    title: "STM Line {{ state_attr('sensor.stm_line_5_blue', 'line_name') }} Alert"
    message: "{{ states('sensor.stm_line_5_blue') }}"
```

### Check number of active alerts

```yaml
{{ state_attr('sensor.stm_line_2_orange', 'alert_count') }}
```

---

## Update from v1.x

Version 2.0.0 moves from the old STM website scraping to the official STM API. You will need to reconfigure the integration with an API key from the [STM Developer Portal](https://portal.stm.info/). Remove the old integration and re-add it with your API key.

---

## Contributing

Contributions are welcome! Fork the repo, make your changes, and submit a PR.

## Credits

- [mattyes](https://github.com/mattyes) – Original script
- [jerji](https://github.com/jerji) – Optimization and addon
- STM – Data (via their [API portal](https://portal.stm.info/))

## Licence

MIT
