from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import DOMAIN
from .coordinator import BoulderweltDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Boulderwelt from a config entry."""
    boulder_hall = entry.data["boulder_hall"]
    # Scan interval can be updated via options flow, fallback to entry data or default 5
    scan_interval = entry.options.get("scan_interval", entry.data.get("scan_interval", 5))

    coordinator = BoulderweltDataUpdateCoordinator(hass, boulder_hall, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Listen for option updates
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(entry.entry_id)
