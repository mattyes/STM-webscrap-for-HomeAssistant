"""Config flow for STM Metro Status integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_API_KEY


@config_entries.HANDLERS.register(DOMAIN)
class STMFlowHandler(config_entries.ConfigFlow):
    """Config flow for STM Metro Status."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            api_key = user_input.get(CONF_API_KEY, "").strip()
            if not api_key:
                errors[CONF_API_KEY] = "required"
            else:
                return self.async_create_entry(
                    title="STM Metro Status",
                    data={CONF_API_KEY: api_key},
                )

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): vol.All(str, vol.Strip),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "message": (
                    "Enter your STM API key to fetch real-time metro status.\n\n"
                    "You can get an API key from the "
                    "[STM Developer Portal](https://portal.stm.info/)."
                )
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return STMOptionsFlowHandler(config_entry)


class STMOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for STM Metro Status."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={CONF_API_KEY: user_input[CONF_API_KEY]},
            )

        current_key = self.config_entry.data.get(CONF_API_KEY, "")

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY, default=current_key): vol.All(str, vol.Strip),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            description_placeholders={
                "key_hint": "Update your STM API key if needed.",
            },
        )