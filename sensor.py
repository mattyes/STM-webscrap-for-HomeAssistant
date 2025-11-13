# custom_components/stm_metro_status/sensor.py
import asyncio
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from .stm_api import fetch_metro_status

_LOGGER = logging.getLogger(__name__)

LINE_SENSORS = {
    "Line 1 - Green": "stm_metro_line_1_status",
    "Line 2 - Orange": "stm_metro_line_2_status",
    "Line 5 - Blue": "stm_metro_line_5_status",
    "Line 4 - Yellow": "stm_metro_line_4_status",
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up STM Metro Status sensors from a config entry."""
    _LOGGER.debug("Setting up STM Metro Status sensors.")
    statuses = await hass.async_add_executor_job(fetch_metro_status)
    sensors = [
        STMMetroSensor(line, statuses.get(line, "Unknown"))
        for line in LINE_SENSORS
    ]
    async_add_entities(sensors, True)

class STMMetroSensor(Entity):
    """Representation of an STM Metro Line Status sensor."""

    def __init__(self, line_name, status):
        self._line_name = line_name
        self._state = status
        self._attr_unique_id = LINE_SENSORS[line_name]
        self._attr_name = f"STM {line_name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return an icon representing the sensor."""
        return "mdi:subway"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        _LOGGER.debug("Updating STM Metro Status for %s", self._line_name)
        statuses = await asyncio.get_event_loop().run_in_executor(None, fetch_metro_status)
        self._state = statuses.get(self._line_name, "Unknown")
