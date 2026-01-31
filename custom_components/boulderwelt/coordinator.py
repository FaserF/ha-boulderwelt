import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import aiohttp_client
from homeassistant.util import dt as dt_util

from .const import DOMAIN, BOULDER_HALL_URLS

_LOGGER = logging.getLogger(__name__)

class BoulderweltDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Boulderwelt data."""

    def __init__(self, hass, boulder_hall, scan_interval):
        """Initialize."""
        self.boulder_hall = boulder_hall
        self.url = BOULDER_HALL_URLS[boulder_hall]

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{boulder_hall}",
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        current_time = dt_util.now().time()

        # Boulderwelt halls are usually closed at night.
        # The API might be down or return static data.
        # Use 00:00 to 07:00 as closed window (Munich halls open at 07:00)
        # Hamburg/Dortmund etc might differ, but this is a safe "night" range.
        if dt_util.parse_time("00:00") <= current_time < dt_util.parse_time("07:00"):
            _LOGGER.debug("Hall is closed (00:00 - 07:00), returning 0%% occupancy")
            return {"level": 0}

        try:
            session = aiohttp_client.async_get_clientsession(self.hass)
            _LOGGER.debug("Fetching data for %s from %s", self.boulder_hall, self.url)

            async with session.get(self.url, timeout=15) as response:
                response.raise_for_status()
                data = await response.json()

                _LOGGER.debug("Received data for %s: %s", self.boulder_hall, data)

                if data.get("success") is True and "level" in data:
                    return data

                _LOGGER.warning("Invalid API response for %s: %s", self.boulder_hall, data)
                return {"level": 0}

        except Exception as err:
            _LOGGER.error("Error fetching data for %s: %s", self.boulder_hall, err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err
