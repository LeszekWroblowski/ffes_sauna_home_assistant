"""Support for FFES Sauna switches."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class FFESSaunaSwitchEntityDescription(SwitchEntityDescription):
    """Describes FFES Sauna switch entity."""

    is_on_fn: Callable[[dict], bool] | None = None
    turn_on_fn: Callable[[FFESSaunaCoordinator], Any] | None = None
    turn_off_fn: Callable[[FFESSaunaCoordinator], Any] | None = None


SWITCHES: tuple[FFESSaunaSwitchEntityDescription, ...] = (
    FFESSaunaSwitchEntityDescription(
        key="light",
        name="Light",
        icon="mdi:lightbulb",
        is_on_fn=lambda data: data.get("light", False),
        turn_on_fn=lambda coord: coord.async_set_light(True),
        turn_off_fn=lambda coord: coord.async_set_light(False),
    ),
    FFESSaunaSwitchEntityDescription(
        key="aux",
        name="AUX",
        icon="mdi:power-plug",
        is_on_fn=lambda data: data.get("aux", False),
        turn_on_fn=lambda coord: coord.async_set_aux(True),
        turn_off_fn=lambda coord: coord.async_set_aux(False),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna switches."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        FFESSaunaSwitch(coordinator, description, entry)
        for description in SWITCHES
    ]
    
    async_add_entities(entities)


class FFESSaunaSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a FFES Sauna switch."""

    entity_description: FFESSaunaSwitchEntityDescription

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        description: FFESSaunaSwitchEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "FFES Sauna",
            "manufacturer": "FFES",
            "model": "Sauna Controller",
        }

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        if self.entity_description.is_on_fn:
            return self.entity_description.is_on_fn(self.coordinator.data)
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        if self.entity_description.turn_on_fn:
            await self.entity_description.turn_on_fn(self.coordinator)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self.entity_description.turn_off_fn:
            await self.entity_description.turn_off_fn(self.coordinator)
