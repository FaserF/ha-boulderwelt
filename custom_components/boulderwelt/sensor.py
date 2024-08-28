import aiohttp
import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN, BOULDER_HALL_URLS

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Boulderwelt sensor based on a config entry."""
    boulder_hall = entry.data.get("boulder_hall")
    url = BOULDER_HALL_URLS[boulder_hall]

    _LOGGER.debug(f"Setting up sensor for {boulder_hall} with URL {url}")

    coordinator = BoulderweltDataUpdateCoordinator(hass, url)
    await coordinator.async_config_entry_first_refresh()

    if coordinator.data is not None:
        _LOGGER.debug(f"Coordinator data is available, adding entity: {boulder_hall}")
        async_add_entities([BoulderweltSensor(coordinator, boulder_hall)], True)
    else:
        _LOGGER.warning(f"Coordinator data is None, no entity added for {boulder_hall}")


class BoulderweltDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, url):
        """Initialize the data updater."""
        self.url = url
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name="Boulderwelt Data",
            update_interval=MIN_TIME_BETWEEN_UPDATES,
        )

    async def _async_update_data(self):
        """Fetch data from API asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                _LOGGER.debug(f"Fetching data from {self.url}")
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug(f"Received data: {data}")
                    return data
        except Exception as e:
            _LOGGER.error(f"Error fetching data from {self.url}: {e}")
            return None


class BoulderweltSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Boulderwelt sensor."""

    def __init__(self, coordinator, name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"{name} Level"
        self._attr_unit_of_measurement = "%"
        self._attr_unique_id = f"boulderwelt_{name.lower().replace(' ', '_')}_level"
        self._attr_icon = "mdi:carabiner"
        self._state = None
        _LOGGER.debug(f"Initialized sensor: {self._attr_name}")

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            level = self.coordinator.data.get("level")
            _LOGGER.debug(f"Returning state for {self._attr_name}: {level}")
            return level
        _LOGGER.debug(f"No data available for {self._attr_name}")
        return None
