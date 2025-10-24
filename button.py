"""Support for FFES Sauna buttons."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATUS_OFF, STATUS_HEATING, STATUS_VENTILATION, STATUS_STANDBY
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class FFESSaunaButtonEntityDescription(ButtonEntityDescription):
    """Describes FFES Sauna button entity."""

    press_fn: Callable[[FFESSaunaCoordinator], Any] | None = None


BUTTONS: tuple[FFESSaunaButtonEntityDescription, ...] = (
    FFESSaunaButtonEntityDescription(
        key="turn_off",
        name="Turn Off",
        icon="mdi:power-off",
        press_fn=lambda coord: coord.async_set_status(STATUS_OFF),
    ),
    FFESSaunaButtonEntityDescription(
        key="start_heating",
        name="Start Heating",
        icon="mdi:fire",
        press_fn=lambda coord: coord.async_set_status(STATUS_HEATING),
    ),
    FFESSaunaButtonEntityDescription(
        key="start_ventilation",
        name="Start Ventilation",
        icon="mdi:fan",
        press_fn=lambda coord: coord.async_set_status(STATUS_VENTILATION),
    ),
    FFESSaunaButtonEntityDescription(
        key="standby",
        name="Standby",
        icon="mdi:pause",
        press_fn=lambda coord: coord.async_set_status(STATUS_STANDBY),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna buttons."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        FFESSaunaButton(coordinator, description, entry)
        for description in BUTTONS
    ]
    
    async_add_entities(entities)


class FFESSaunaButton(CoordinatorEntity, ButtonEntity):
    """Representation of a FFES Sauna button."""

    entity_description: FFESSaunaButtonEntityDescription

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        description: FFESSaunaButtonEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "FFES Sauna",
            "manufacturer": "FFES",
            "model": "Sauna Controller",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        if self.entity_description.press_fn:
            await self.entity_description.press_fn(self.coordinator)
