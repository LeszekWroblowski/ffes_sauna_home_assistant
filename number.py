"""Support for FFES Sauna number entities."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MIN_TEMP, MAX_TEMP, MIN_HUMIDITY, MAX_HUMIDITY, PROFILE_REVERSE_MAP
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class FFESSaunaNumberEntityDescription(NumberEntityDescription):
    """Describes FFES Sauna number entity."""

    value_fn: Callable[[dict], float | None] | None = None


NUMBERS: tuple[FFESSaunaNumberEntityDescription, ...] = (
    FFESSaunaNumberEntityDescription(
        key="target_temperature",
        name="Target Temperature",
        icon="mdi:thermometer",
        native_min_value=MIN_TEMP,
        native_max_value=MAX_TEMP,
        native_step=1,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        value_fn=lambda data: data.get("setTemp"),
    ),
    FFESSaunaNumberEntityDescription(
        key="humidity_setting",
        name="Humidity Setting",
        icon="mdi:water-percent",
        native_min_value=MIN_HUMIDITY,
        native_max_value=MAX_HUMIDITY,
        native_step=5,
        native_unit_of_measurement=PERCENTAGE,
        mode=NumberMode.SLIDER,
        value_fn=lambda data: data.get("humidityValue"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna number entities."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        FFESSaunaNumber(coordinator, description, entry)
        for description in NUMBERS
    ]
    
    async_add_entities(entities)


class FFESSaunaNumber(CoordinatorEntity, NumberEntity):
    """Representation of a FFES Sauna number entity."""

    entity_description: FFESSaunaNumberEntityDescription

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        description: FFESSaunaNumberEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
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
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        # Get current settings
        data = self.coordinator.data
        profile_name = data.get("profile", 2)
        
        session_time_raw = data.get("sessionTime", 130)
        hours = session_time_raw // 100
        minutes = session_time_raw % 100
        session_time = f"{hours:02d}:{minutes:02d}"
        
        if self.entity_description.key == "target_temperature":
            temperature = int(value)
            humidity_value = data.get("humidityValue", 0)
        else:  # humidity_setting
            temperature = data.get("setTemp", 80)
            humidity_value = int(value)
        
        # Start session with new settings
        await self.coordinator.async_start_session(
            profile=profile_name,
            temperature=temperature,
            session_time=session_time,
            humidity_value=humidity_value,
        )
