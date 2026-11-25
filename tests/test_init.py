from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from custom_components.boulderwelt.coordinator import BoulderweltDataUpdateCoordinator


async def test_coordinator_update_data_success(hass: HomeAssistant):
    """Test successful data update from coordinator."""
    # Mock time to be 10:00 AM so API is called
    test_time = dt_util.parse_datetime("2024-01-01 10:00:00")

    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with (
        patch(
            "homeassistant.helpers.aiohttp_client.async_get_clientsession"
        ) as mock_session,
        patch("homeassistant.util.dt.now", return_value=test_time),
    ):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"level": 50, "success": True})
        mock_response.raise_for_status = MagicMock()

        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )

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

    with (
        patch(
            "homeassistant.helpers.aiohttp_client.async_get_clientsession"
        ) as mock_session,
        patch("homeassistant.util.dt.now", return_value=test_time),
    ):
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.raise_for_status.side_effect = Exception("API Error")

        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )

        from homeassistant.helpers.update_coordinator import UpdateFailed

        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()


async def test_coordinator_update_data_api_success_false(hass: HomeAssistant):
    """Test data update when API returns success: False."""
    test_time = dt_util.parse_datetime("2024-01-01 10:00:00")
    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with (
        patch(
            "homeassistant.helpers.aiohttp_client.async_get_clientsession"
        ) as mock_session,
        patch("homeassistant.util.dt.now", return_value=test_time),
    ):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"level": 0, "success": False})
        mock_response.raise_for_status = MagicMock()

        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )

        data = await coordinator._async_update_data()
        assert data["level"] == 0
        assert data["success"] is False


async def test_coordinator_update_data_timeout_retry_success(hass: HomeAssistant):
    """Test transient timeout retries once and succeeds on second attempt."""
    test_time = dt_util.parse_datetime("2024-01-01 10:00:00")
    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with (
        patch(
            "homeassistant.helpers.aiohttp_client.async_get_clientsession"
        ) as mock_session,
        patch("homeassistant.util.dt.now", return_value=test_time),
    ):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"level": 42, "success": True})
        mock_response.raise_for_status = MagicMock()

        first_ctx = MagicMock()
        first_ctx.__aenter__ = AsyncMock(side_effect=TimeoutError("timed out"))
        second_ctx = MagicMock()
        second_ctx.__aenter__ = AsyncMock(return_value=mock_response)
        second_ctx.__aexit__ = AsyncMock(return_value=False)

        mock_session.return_value.get.side_effect = [first_ctx, second_ctx]

        data = await coordinator._async_update_data()
        assert data["level"] == 42
        assert mock_session.return_value.get.call_count == 2


async def test_coordinator_update_data_timeout_exhausted(hass: HomeAssistant):
    """Test repeated timeout raises UpdateFailed after retries."""
    from homeassistant.helpers.update_coordinator import UpdateFailed

    test_time = dt_util.parse_datetime("2024-01-01 10:00:00")
    coordinator = BoulderweltDataUpdateCoordinator(hass, "Boulderwelt München Ost", 5)

    with (
        patch(
            "homeassistant.helpers.aiohttp_client.async_get_clientsession"
        ) as mock_session,
        patch("homeassistant.util.dt.now", return_value=test_time),
    ):
        timeout_ctx = MagicMock()
        timeout_ctx.__aenter__ = AsyncMock(side_effect=TimeoutError("still timed out"))
        mock_session.return_value.get.return_value = timeout_ctx

        with pytest.raises(UpdateFailed, match="Timeout communicating with API"):
            await coordinator._async_update_data()
        assert mock_session.return_value.get.call_count == 2
