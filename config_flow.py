# custom_components/stm_metro_status/config_flow.py
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from . import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class STMFlowHandler(config_entries.ConfigFlow):
    """Config flow for STM Metro Status."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            # No user input required; just create the entry
            return self.async_create_entry(title="STM Metro Status", data={})

        # Show a simple message in the UI
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={
                "message": "This integration will add the STM line status to Home assistant. Click submit to continue."
            }
        )