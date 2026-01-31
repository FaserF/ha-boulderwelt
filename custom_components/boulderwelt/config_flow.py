import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, BOULDER_HALLS

class BoulderweltConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Boulderwelt."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Check if already configured
            await self.async_set_unique_id(user_input["boulder_hall"])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input["boulder_hall"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("boulder_hall"): vol.In(sorted(BOULDER_HALLS)),
                vol.Optional("scan_interval", default=5): vol.All(cv.positive_int, vol.Clamp(min=1, max=60))
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return BoulderweltOptionsFlowHandler(config_entry)


class BoulderweltOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Boulderwelt."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get(
                        "scan_interval",
                        self.config_entry.data.get("scan_interval", 5)
                    )
                ): vol.All(cv.positive_int, vol.Clamp(min=1, max=60))
            })
        )
