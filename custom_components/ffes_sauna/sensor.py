"""Support for FFES Sauna sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PROFILES, STATUS_MAP
from .coordinator import FFESSaunaCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class FFESSaunaSensorEntityDescription(SensorEntityDescription):
    """Describes FFES Sauna sensor entity."""

    value_fn: Callable[[dict], StateType] | None = None


SENSORS: tuple[FFESSaunaSensorEntityDescription, ...] = (
    FFESSaunaSensorEntityDescription(
        key="actualTemp",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("actualTemp"),
    ),
    FFESSaunaSensorEntityDescription(
        key="humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("humidity"),
    ),
    FFESSaunaSensorEntityDescription(
        key="setTemp",
        name="Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="mdi:thermometer-chevron-up",
        value_fn=lambda data: data.get("setTemp"),
    ),
    FFESSaunaSensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:sauna",
        value_fn=lambda data: STATUS_MAP.get(data.get("controllerStatus", 0), "unknown"),
    ),
    FFESSaunaSensorEntityDescription(
        key="profile",
        name="Profile",
        icon="mdi:format-list-bulleted",
        value_fn=lambda data: PROFILES.get(data.get("profile", 0), "Unknown"),
    ),
    FFESSaunaSensorEntityDescription(
        key="sessionTime",
        name="Session Time",
        icon="mdi:clock-outline",
        value_fn=lambda data: _format_time(data.get("sessionTime", 0)),
    ),
    FFESSaunaSensorEntityDescription(
        key="ventilationTime",
        name="Ventilation Time",
        icon="mdi:fan-clock",
        value_fn=lambda data: _format_time(data.get("ventilationTime", 0)),
    ),
    FFESSaunaSensorEntityDescription(
        key="aromaValue",
        name="Aromatherapy",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:flower",
        value_fn=lambda data: data.get("aromaValue"),
    ),
    FFESSaunaSensorEntityDescription(
        key="humidityValue",
        name="Humidity Setting",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:water-percent",
        value_fn=lambda data: data.get("humidityValue"),
    ),
)


def _format_time(time_value: int) -> str:
    """Format time from integer to HH:MM string."""
    if not time_value:
        return "00:00"
    hours = time_value // 100
    minutes = time_value % 100
    return f"{hours:02d}:{minutes:02d}"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FFES Sauna sensors."""
    coordinator: FFESSaunaCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        FFESSaunaSensor(coordinator, description, entry)
        for description in SENSORS
    ]
    
    async_add_entities(entities)


class FFESSaunaSensor(CoordinatorEntity, SensorEntity):
    """Representation of a FFES Sauna sensor."""

    entity_description: FFESSaunaSensorEntityDescription

    def __init__(
        self,
        coordinator: FFESSaunaCoordinator,
        description: FFESSaunaSensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
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
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None
