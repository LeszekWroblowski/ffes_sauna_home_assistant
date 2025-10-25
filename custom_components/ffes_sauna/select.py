"""Support for FFES Sauna select entities."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PROFILES, PROFILE_REVERSE_MAP
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna select entities."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([FFESSaunaProfileSelect(coordinator, entry)])


class FFESSaunaProfileSelect(CoordinatorEntity, SelectEntity):
    """Representation of FFES Sauna profile selector."""

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_name = "Profile"
        self._attr_unique_id = f"{entry.entry_id}_profile_select"
        self._attr_icon = "mdi:format-list-bulleted"
        self._attr_options = list(PROFILES.values())
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "FFES Sauna",
            "manufacturer": "FFES",
            "model": "Sauna Controller",
        }

    @property
    def current_option(self) -> str | None:
        """Return the selected option."""
        profile_id = self.coordinator.data.get("profile")
        return PROFILES.get(profile_id, list(PROFILES.values())[0])

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        profile_id = PROFILE_REVERSE_MAP.get(option)
        if profile_id is None:
            _LOGGER.error("Unknown profile: %s", option)
            return
        
        # Get current settings
        temperature = self.coordinator.data.get("setTemp", 80)
        session_time_raw = self.coordinator.data.get("sessionTime", 130)
        
        # Format session time
        hours = session_time_raw // 100
        minutes = session_time_raw % 100
        session_time = f"{hours:02d}:{minutes:02d}"
        
        # Start session with new profile
        await self.coordinator.async_start_session(
            profile=profile_id,
            temperature=temperature,
            session_time=session_time,
        )
