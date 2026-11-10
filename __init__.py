"""STM Metro Status integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up STM Metro Status from a config entry."""
    # Store the config in hass.data so other platforms can access it
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entry to a new version."""
    _LOGGER.debug("Migrating config entry from version %s", entry.version)

    if entry.version == 1:
        # Version 1 -> 2: added API key requirement
        new_data = {**entry.data}
        if CONF_API_KEY not in new_data:
            # Old entries didn't have an API key; we can't function without one
            new_data[CONF_API_KEY] = ""

        hass.config_entries.async_update_entry(entry, data=new_data, version=2)

    _LOGGER.debug("Migration to version %s successful", entry.version)
    return True