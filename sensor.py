"""Sensor platform for STM Metro Status."""
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, CONF_API_KEY
from .stm_api import fetch_metro_alerts

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

LINE_SENSORS = {
    "Line 1 - Green": "stm_metro_line_1_status",
    "Line 2 - Orange": "stm_metro_line_2_status",
    "Line 4 - Yellow": "stm_metro_line_4_status",
    "Line 5 - Blue": "stm_metro_line_5_status",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up STM Metro Status sensors from a config entry."""
    _LOGGER.debug("Setting up STM Metro Status sensors")

    api_key = entry.data.get(CONF_API_KEY, "")
    if not api_key:
        _LOGGER.error("No API key configured for STM Metro Status")
        return

    coordinator = STMDataCoordinator(hass, api_key)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        STMMetroSensor(coordinator, line_name, unique_id)
        for line_name, unique_id in LINE_SENSORS.items()
    ]
    async_add_entities(sensors, True)


class STMDataCoordinator(DataUpdateCoordinator):
    """Fetch STM data and keep it fresh."""

    def __init__(self, hass: HomeAssistant, api_key: str):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="STM Metro Status",
            update_interval=SCAN_INTERVAL,
        )
        self.api_key = api_key

    async def _async_update_data(self):
        """Fetch data from the STM API."""
        data = await self.hass.async_add_executor_job(
            fetch_metro_alerts, self.api_key
        )
        if not data:
            raise UpdateFailed("No data received from STM API")
        return data


class STMMetroSensor(CoordinatorEntity, SensorEntity):
    """Representation of an STM Metro Line Status sensor."""

    def __init__(self, coordinator, line_name, unique_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._line_name = line_name
        self._attr_unique_id = unique_id
        self._attr_name = f"STM {line_name}"
        self._attr_icon = "mdi:subway"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        data = self.coordinator.data or {}
        line_data = data.get(self._line_name, {})
        return line_data.get("state", "Unknown")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        data = self.coordinator.data or {}
        line_data = data.get(self._line_name, {})
        return {
            "line_name": self._line_name,
            "has_alerts": line_data.get("has_alerts", False),
        }

    @property
    def available(self):
        """Return if the sensor is available."""
        return self.coordinator.last_update_success