"""File-based storage implementation."""

import logging
import os
from typing import Optional

from motorcycle_alert.domain.models import MotorcycleStatus
from motorcycle_alert.domain.services import StatusStorage

logger = logging.getLogger(__name__)


class FileStatusStorage(StatusStorage):
    """File-based implementation of status storage."""

    def __init__(self, file_path: str):
        """Initialize the storage with file path."""
        self._file_path = file_path

    def load_last_status(self) -> Optional[MotorcycleStatus]:
        """Load the last known status from file."""
        if not os.path.exists(self._file_path):
            logger.debug(f"Status file {self._file_path} does not exist")
            return None

        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return None

                # Parse the saved status format: icon_color,alimentation,blocked,ignition
                parts = content.split(",")
                if len(parts) >= 4:
                    return MotorcycleStatus(
                        icon_color=parts[0],
                        alimentation=parts[1],
                        blocked=parts[2].lower() == "true",
                        ignition=parts[3],
                    )

        except (IOError, ValueError) as e:
            logger.error(f"Failed to load status from {self._file_path}: {e}")

        return None

    def save_status(self, status: MotorcycleStatus) -> None:
        """Save the current status to file."""
        try:
            with open(self._file_path, "w", encoding="utf-8") as file:
                content = f"{status.icon_color},{status.alimentation},{status.blocked},{status.ignition}"
                file.write(content)

            logger.debug(f"Status saved to {self._file_path}")

        except IOError as e:
            logger.error(f"Failed to save status to {self._file_path}: {e}")
            raise
