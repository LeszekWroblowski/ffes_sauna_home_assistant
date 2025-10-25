"""DataUpdateCoordinator for FFES Sauna."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, ENDPOINT_DATA, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class FFESSaunaCoordinator(DataUpdateCoordinator):
    """Class to manage fetching FFES Sauna data."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize."""
        self.host = host
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        url = f"{self.host}{ENDPOINT_DATA}"
        
        try:
            async with self.session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"HTTP {response.status}")
                
                data = await response.json()
                _LOGGER.debug("Received data: %s", data)
                return data
                
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_set_status(self, status: int) -> bool:
        """Set sauna status."""
        return await self._async_send_command("status", status)

    async def async_set_light(self, state: bool) -> bool:
        """Set light state."""
        return await self._async_send_command("light", 1 if state else 0)

    async def async_set_aux(self, state: bool) -> bool:
        """Set AUX state."""
        return await self._async_send_command("aux", 1 if state else 0)

    async def async_start_session(
        self,
        profile: int,
        temperature: int,
        session_time: str,
        ventilation_time: str = "00:15",
        aroma_value: int = 0,
        humidity_value: int = 0,
    ) -> bool:
        """Start a sauna session."""
        data = {
            "action": "start_session",
            "profile": str(profile),
            "temperature": str(temperature),
            "session_time": session_time,
            "ventilation_time": ventilation_time,
            "aroma_value": str(aroma_value),
            "humidity_value": str(humidity_value),
        }
        
        return await self._async_send_post(data)

    async def _async_send_command(self, action: str, value: int) -> bool:
        """Send a command to the sauna controller."""
        data = {
            "action": action,
            "value": str(value),
        }
        
        return await self._async_send_post(data)

    async def _async_send_post(self, data: dict[str, str]) -> bool:
        """Send POST request to controller."""
        from .const import ENDPOINT_CONTROL
        
        url = f"{self.host}{ENDPOINT_CONTROL}"
        
        try:
            async with self.session.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to send command: HTTP %s", response.status)
                    return False
                
                result = await response.json()
                success = result.get("success", False)
                
                if not success:
                    _LOGGER.error("Command failed: %s", result.get("message", "Unknown error"))
                
                # Request immediate data refresh
                await self.async_request_refresh()
                
                return success
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Error sending command: %s", err)
            return False
        except Exception as err:
            _LOGGER.exception("Unexpected error sending command: %s", err)
            return False
