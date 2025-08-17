"""Application use cases for motorcycle alert system."""

import asyncio
import logging

from motorcycle_alert.domain.services import (
    MotorcycleAlertService,
    MotorcycleDataRepository,
    NotificationService,
    StatusStorage,
)

logger = logging.getLogger(__name__)


class MotorcycleMonitoringUseCase:
    """Use case for monitoring motorcycle status."""

    def __init__(
        self,
        data_repository: MotorcycleDataRepository,
        status_storage: StatusStorage,
        notification_service: NotificationService,
        check_interval: int = 60,
    ):
        """Initialize the monitoring use case."""
        self._alert_service = MotorcycleAlertService(
            data_repository, status_storage, notification_service
        )
        self._check_interval = check_interval
        self._running = False

    async def start_monitoring(self) -> None:
        """Start continuous monitoring of motorcycle status."""
        logger.info("Starting motorcycle monitoring...")
        self._running = True

        while self._running:
            try:
                await self._alert_service.check_and_alert()
                logger.debug("Status check completed successfully")
            except Exception as e:
                logger.error(f"Error during status check: {e}")

            await asyncio.sleep(self._check_interval)

    def stop_monitoring(self) -> None:
        """Stop the monitoring process."""
        logger.info("Stopping motorcycle monitoring...")
        self._running = False
