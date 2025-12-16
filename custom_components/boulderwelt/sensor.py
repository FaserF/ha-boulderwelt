import aiohttp
import logging
from homeassistant.helpers import aiohttp_client
from datetime import timedelta, datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN, BOULDER_HALL_URLS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Boulderwelt sensor based on a config entry."""
    boulder_hall = entry.data.get("boulder_hall")
    url = BOULDER_HALL_URLS[boulder_hall]
    scan_interval = entry.data.get("scan_interval", 5)

    _LOGGER.debug(f"Setting up sensor for {boulder_hall} with URL {url} and scan_interval {scan_interval} minutes")

    coordinator = BoulderweltDataUpdateCoordinator(hass, url, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    if coordinator.data is not None:
        _LOGGER.debug(f"Coordinator data is available, adding entity: {boulder_hall}")
        async_add_entities([BoulderweltSensor(coordinator, boulder_hall)], True)
    else:
        _LOGGER.warning(f"Coordinator data is None, no entity added for {boulder_hall}")

class BoulderweltDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, url, scan_interval):
        """Initialize the data updater."""
        self.url = url
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name="Boulderwelt Data",
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self):
        """Fetch data from API asynchronously."""
        current_time = datetime.now().time()
        if current_time >= datetime.strptime("00:00", "%H:%M").time() and current_time < datetime.strptime("08:00", "%H:%M").time():
            _LOGGER.debug("Current time is between 00:00 and 08:00, returning 0% usage.")
            return {"level": 0}  # Returning 0% usage instead of fetching data
        try:
            session = aiohttp_client.async_get_clientsession(self.hass)
            _LOGGER.debug(f"Fetching data from {self.url}")
            async with session.get(self.url) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug(f"Received data: {data}")
                if "level" in data and data.get("success", False):
                    return data
                else:
                    _LOGGER.debug("Data is missing 'level' or 'success' is False, defaulting to 0")
                    return {"level": 0}
        except Exception as e:
            _LOGGER.error(f"Error fetching data from {self.url}: {e}")
            _LOGGER.debug("Returning default value 0 due to exception")
            return {"level": 0}

class BoulderweltSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Boulderwelt sensor."""

    def __init__(self, coordinator, name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"{name} Level"
        self._attr_unit_of_measurement = PERCENTAGE
        self._attr_unique_id = f"boulderwelt_{name.lower().replace(' ', '_')}_level"
        self._attr_icon = "mdi:carabiner"
        _LOGGER.debug(f"Initialized sensor: {self._attr_name}")

    @property
    def state(self):
        """Return the state of the sensor."""
        level = self.coordinator.data.get("level")

        # Get the current hour
        current_hour = datetime.now().hour

        # Check if the current time is between 0 and 5 hours
        if level is None or (level == 0 and 0 <= current_hour < 5):
            _LOGGER.debug(f"Returning default value 0 for {self._attr_name} because it's between 0 and 5 AM and the API most likely is shut off.")
            return 0
        elif level is None:
            _LOGGER.debug(f"Returning unknown for {self._attr_name} because level is None")
            return None
        else:
            _LOGGER.debug(f"Returning state for {self._attr_name}: {level}")
            return level
