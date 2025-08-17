"""HTTP client for motorcycle data API."""

import logging
from datetime import datetime
from typing import Any, Dict

import requests

from motorcycle_alert.domain.models import MotorcycleStatus
from motorcycle_alert.domain.services import MotorcycleDataRepository
from motorcycle_alert.infrastructure.config import Config, get_api_headers

logger = logging.getLogger(__name__)


class ApiMotorcycleDataRepository(MotorcycleDataRepository):
    """Implementation of motorcycle data repository using HTTP API."""

    def __init__(self, config: Config):
        """Initialize the repository with configuration."""
        self._config = config
        self._headers = get_api_headers()

    async def get_current_status(self) -> MotorcycleStatus:
        """Get current motorcycle status from external API."""
        try:
            ts_ms = int(datetime.now().timestamp() * 1000)
            url = f"{self._config.api_base_url}/objects/items?id={self._config.object_id}&full=true&_={ts_ms}"

            logger.debug(f"Fetching motorcycle data from: {url}")

            response = requests.get(url, headers=self._headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            return self._parse_api_response(data)

        except requests.RequestException as e:
            logger.error(f"Failed to fetch motorcycle data: {e}")
            raise
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse API response: {e}")
            raise

    def _parse_api_response(self, data: Dict[str, Any]) -> MotorcycleStatus:
        """Parse API response into MotorcycleStatus domain model."""
        if not data.get("data") or not data["data"]:
            raise ValueError("Invalid API response: no data found")

        item_data = data["data"][0]

        # Extract basic fields
        icon_color = item_data.get("icon_color", "")
        time_mt = item_data.get("time", "")
        stop_duration = item_data.get("stop_duration", "")
        speed = item_data.get("speed", "")

        # Parse sensors
        sensors = self._parse_sensors(item_data.get("sensors", []))

        return MotorcycleStatus(
            icon_color=icon_color,
            alimentation=sensors.get("alimentation", ""),
            blocked=sensors.get("blocked", False),
            ignition=sensors.get("ignition", ""),
            time=time_mt,
            stop_duration=stop_duration,
            speed=speed,
            additional_sensors={
                k: v
                for k, v in sensors.items()
                if k not in ["alimentation", "blocked", "ignition"]
            },
        )

    def _parse_sensors(self, sensors_data: list) -> Dict[str, Any]:
        """Parse sensors data from API response."""
        sensors = {}

        for sensor in sensors_data:
            name = sensor.get("name", "").lower().strip()
            value = sensor.get("value")

            if not name or value is None:
                continue

            # Map known sensor names to standard names
            if name == "alimentacao":
                sensors["alimentation"] = value
            elif name == "ignicao":
                sensors["ignition"] = value
            elif name == "bloqueio":
                sensors["blocked"] = bool(value.lower() != "desligado")
            else:
                sensors[name] = value

        return sensors
