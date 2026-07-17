"""Time entities for Dreame Mower allowed charging schedule."""

from __future__ import annotations

from datetime import time
import logging

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import DreameMowerCoordinator
from .entity import DreameMowerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Dreame Mower times from a config entry."""
    coordinator: DreameMowerCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities(
        [
            DreameMowerChargingStartTimeEntity(coordinator),
            DreameMowerChargingEndTimeEntity(coordinator),
        ]
    )


class DreameMowerChargingStartTimeEntity(DreameMowerEntity, TimeEntity):
    """Time entity for allowed charging start time."""

    def __init__(self, coordinator: DreameMowerCoordinator) -> None:
        """Initialize the charging start time entity."""
        super().__init__(coordinator, "charging_start_time")
        self._attr_name = "Charging Start Time"
        self._attr_icon = "mdi:clock-start"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "battery_config_values": self.coordinator.device.battery_config_values,
        }

    @property
    def native_value(self) -> time | None:
        """Return the value reported by the time entity."""
        start_time_str = self.coordinator.device.charging_start_time
        if start_time_str is None:
            return None
        try:
            parts = [int(p) for p in start_time_str.split(":")]
            return time(parts[0], parts[1])
        except (ValueError, IndexError):
            return None

    async def async_set_value(self, value: time) -> None:
        """Set the time."""
        start_time = f"{value.hour:02d}:{value.minute:02d}"
        
        # We need the current end time to perform the set call
        end_time_str = self.coordinator.device.charging_end_time or "08:00"
        enabled = self.coordinator.device.custom_charging_enabled
        if enabled is None:
            enabled = True

        await self.coordinator.device.set_charging_times(start_time, end_time_str, enabled)
        await self.coordinator.async_request_refresh()


class DreameMowerChargingEndTimeEntity(DreameMowerEntity, TimeEntity):
    """Time entity for allowed charging end time."""

    def __init__(self, coordinator: DreameMowerCoordinator) -> None:
        """Initialize the charging end time entity."""
        super().__init__(coordinator, "charging_end_time")
        self._attr_name = "Charging End Time"
        self._attr_icon = "mdi:clock-end"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "battery_config_values": self.coordinator.device.battery_config_values,
        }

    @property
    def native_value(self) -> time | None:
        """Return the value reported by the time entity."""
        end_time_str = self.coordinator.device.charging_end_time
        if end_time_str is None:
            return None
        try:
            parts = [int(p) for p in end_time_str.split(":")]
            return time(parts[0], parts[1])
        except (ValueError, IndexError):
            return None

    async def async_set_value(self, value: time) -> None:
        """Set the time."""
        end_time = f"{value.hour:02d}:{value.minute:02d}"
        
        # We need the current start time to perform the set call
        start_time_str = self.coordinator.device.charging_start_time or "22:00"
        enabled = self.coordinator.device.custom_charging_enabled
        if enabled is None:
            enabled = True

        await self.coordinator.device.set_charging_times(start_time_str, end_time, enabled)
        await self.coordinator.async_request_refresh()
