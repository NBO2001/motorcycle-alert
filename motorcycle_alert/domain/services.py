"""Domain services for motorcycle alert system."""

from abc import ABC, abstractmethod
from typing import Optional

from motorcycle_alert.domain.models import AlertMessage, MotorcycleStatus


class MotorcycleDataRepository(ABC):
    """Abstract repository for motorcycle data."""

    @abstractmethod
    async def get_current_status(self) -> MotorcycleStatus:
        """Get current motorcycle status from external source."""
        pass


class StatusStorage(ABC):
    """Abstract storage for motorcycle status."""

    @abstractmethod
    def load_last_status(self) -> Optional[MotorcycleStatus]:
        """Load the last known status."""
        pass

    @abstractmethod
    def save_status(self, status: MotorcycleStatus) -> None:
        """Save the current status."""
        pass


class NotificationService(ABC):
    """Abstract notification service."""

    @abstractmethod
    def send_alert(self, message: AlertMessage) -> None:
        """Send alert notification."""
        pass


class MotorcycleAlertService:
    """Domain service for handling motorcycle alerts."""

    def __init__(
        self,
        data_repository: MotorcycleDataRepository,
        status_storage: StatusStorage,
        notification_service: NotificationService,
    ):
        """Initialize the alert service with dependencies."""
        self._data_repository = data_repository
        self._status_storage = status_storage
        self._notification_service = notification_service

    async def check_and_alert(self) -> None:
        """Check for status changes and send alerts if needed."""
        current_status = await self._data_repository.get_current_status()
        last_status = self._status_storage.load_last_status()

        if last_status != current_status:
            self._status_storage.save_status(current_status)

            from datetime import datetime

            alert_message = AlertMessage(
                status=current_status,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            self._notification_service.send_alert(alert_message)
