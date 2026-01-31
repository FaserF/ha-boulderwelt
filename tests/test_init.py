import pytest
from unittest.mock import patch, MagicMock
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from custom_components.boulderwelt.const import DOMAIN
from custom_components.boulderwelt.coordinator import BoulderweltDataUpdateCoordinator

async def test_coordinator_update_data_success(hass: HomeAssistant):
    """Test successful data update from coordinator."""
    # Mock time to be 10:00 AM so API is called
    test_time = dt_util.parse_datetime("2024-01-01 10:00:00")

    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with patch("homeassistant.helpers.aiohttp_client.async_get_clientsession") as mock_session, \
         patch("homeassistant.util.dt.now", return_value=test_time):

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = pytest.AsyncMock(return_value={"level": 50, "success": True})
        mock_response.raise_for_status = MagicMock()

        mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

        data = await coordinator._async_update_data()
        assert data["level"] == 50
        assert data["success"] is True

async def test_coordinator_update_data_night(hass: HomeAssistant):
    """Test data update during night returns 0%."""
    # Mock time to be 02:00 AM
    test_time = dt_util.parse_datetime("2024-01-01 02:00:00")

    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with patch("homeassistant.util.dt.now", return_value=test_time):
        data = await coordinator._async_update_data()
        assert data["level"] == 0

async def test_coordinator_update_data_fail(hass: HomeAssistant):
    """Test failed data update from coordinator."""
    test_time = dt_util.parse_datetime("2024-01-01 10:00:00")
    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with patch("homeassistant.helpers.aiohttp_client.async_get_clientsession") as mock_session, \
         patch("homeassistant.util.dt.now", return_value=test_time):

        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.raise_for_status.side_effect = Exception("API Error")

        mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

        from homeassistant.helpers.update_coordinator import UpdateFailed
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()
