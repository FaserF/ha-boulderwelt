from unittest.mock import patch, MagicMock
import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant

from custom_components.boulderwelt.const import DOMAIN

async def test_config_flow_user_step(hass: HomeAssistant):
    """Test the user step of the config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch("custom_components.boulderwelt.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"boulder_hall": "Boulderwelt München Ost", "scan_interval": 10},
        )

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == "Boulderwelt München Ost"
    assert result["data"] == {"boulder_hall": "Boulderwelt München Ost", "scan_interval": 10}

async def test_config_flow_duplicate(hass: HomeAssistant):
    """Test duplicate entry logic (uniqueness test)."""
    with patch(
        "custom_components.boulderwelt.config_flow.BoulderweltConfigFlow.async_set_unique_id",
        return_value=None,
    ), patch(
        "custom_components.boulderwelt.config_flow.BoulderweltConfigFlow._abort_if_unique_id_configured",
        side_effect=data_entry_flow.AbortFlow("already_configured"),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data={"boulder_hall": "Boulderwelt München Ost", "scan_interval": 10},
        )

    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "already_configured"
