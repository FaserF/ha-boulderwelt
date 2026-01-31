import logging
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTRIBUTION

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Boulderwelt sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    boulder_hall = entry.data["boulder_hall"]

    async_add_entities([BoulderweltSensor(coordinator, boulder_hall, entry.entry_id)], True)

class BoulderweltSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Boulderwelt occupancy sensor."""

    _attr_has_entity_name = True
    _attr_translation_key = "occupancy"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:carabiner"

    def __init__(self, coordinator, name, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name = name
        self._attr_extra_state_attributes = {
            "attribution": ATTRIBUTION,
            "hall_name": name
        }
        self._attr_unique_id = f"{entry_id}_occupancy"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": name,
            "manufacturer": "Boulderwelt",
            "model": "Crowd Indicator",
            "configuration_url": self.coordinator.url,
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("level")
