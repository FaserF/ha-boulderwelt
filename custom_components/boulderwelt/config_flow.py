import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, BOULDER_HALLS

@config_entries.HANDLERS.register(DOMAIN)
class BoulderweltConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["boulder_hall"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("boulder_hall"): vol.In(BOULDER_HALLS)
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BoulderweltOptionsFlowHandler(config_entry)


class BoulderweltOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("boulder_hall", default=self.config_entry.data.get("boulder_hall")): vol.In(BOULDER_HALLS)
            })
        )

        if user_input is not None:
            self.hass.config_entries.async_update_entry(self.config_entry, data=user_input)
            return self.async_create_entry(title="", data={})
