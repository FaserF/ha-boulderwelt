import logging
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTRIBUTION

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Boulderwelt binary sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    boulder_hall = entry.data["boulder_hall"]

    async_add_entities([BoulderweltHighOccupancySensor(coordinator, boulder_hall, entry.entry_id)], True)

class BoulderweltHighOccupancySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Boulderwelt high occupancy binary sensor."""

    _attr_has_entity_name = True
    _attr_translation_key = "highly_occupied"
    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    def __init__(self, coordinator, name, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name = name
        self._attr_unique_id = f"{entry_id}_high_occupancy"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": name,
            "manufacturer": "Boulderwelt",
            "model": "Crowd Indicator",
            "configuration_url": self.coordinator.url,
        }

    @property
    def is_on(self):
        """Return true if the hall is highly occupied."""
        if self.coordinator.data is None:
            return None

        level = self.coordinator.data.get("level", 0)
        # Threshold for highly occupied (75% as default)
        return level >= 75

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "hall_name": self._name,
            "threshold": 75
        }
