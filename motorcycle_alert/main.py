"""Main application entry point."""

import asyncio
import logging
import signal
import sys
from typing import Optional

import dotenv

from motorcycle_alert.application.use_cases import MotorcycleMonitoringUseCase
from motorcycle_alert.infrastructure.api_client import ApiMotorcycleDataRepository
from motorcycle_alert.infrastructure.config import load_config
from motorcycle_alert.infrastructure.notifications import TelegramNotificationService
from motorcycle_alert.infrastructure.storage import FileStatusStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("motorcycle_alert.log"),
    ],
)

logger = logging.getLogger(__name__)


class MotorcycleAlertApplication:
    """Main application class."""

    def __init__(self):
        """Initialize the application."""
        self._monitoring_use_case: Optional[MotorcycleMonitoringUseCase] = None
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        if self._monitoring_use_case:
            self._monitoring_use_case.stop_monitoring()

    async def run(self):
        """Run the application."""
        try:
            # Load environment variables
            dotenv.load_dotenv()

            # Load configuration
            config = load_config()
            logger.info("Configuration loaded successfully")

            # Initialize dependencies
            data_repository = ApiMotorcycleDataRepository(config)
            status_storage = FileStatusStorage(config.status_file_path)
            notification_service = TelegramNotificationService(config)

            # Initialize use case
            self._monitoring_use_case = MotorcycleMonitoringUseCase(
                data_repository=data_repository,
                status_storage=status_storage,
                notification_service=notification_service,
                check_interval=config.check_interval,
            )

            # Start monitoring
            await self._monitoring_use_case.start_monitoring()

        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise


async def main():
    """Main entry point."""
    app = MotorcycleAlertApplication()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
