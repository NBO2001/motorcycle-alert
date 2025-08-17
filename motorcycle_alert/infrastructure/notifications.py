"""Telegram notification service implementation."""

import logging

import telebot

from motorcycle_alert.domain.models import AlertMessage
from motorcycle_alert.domain.services import NotificationService
from motorcycle_alert.infrastructure.config import Config

logger = logging.getLogger(__name__)


class TelegramNotificationService(NotificationService):
    """Telegram-based implementation of notification service."""

    def __init__(self, config: Config):
        """Initialize the notification service with configuration."""
        self._config = config
        self._bot = telebot.TeleBot(config.telegram_api_key)

    def send_alert(self, message: AlertMessage) -> None:
        """Send alert notification via Telegram."""
        try:
            formatted_message = message.format_message()

            self._bot.send_message(
                self._config.telegram_user_id,
                formatted_message,
                parse_mode=(
                    "HTML" if self._should_use_html_parsing(formatted_message) else None
                ),
            )

            logger.info(
                f"Alert sent successfully to user {self._config.telegram_user_id}"
            )

        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            raise

    def _should_use_html_parsing(self, message: str) -> bool:
        """Determine if HTML parsing should be used for the message."""
        # Simple check to see if the message contains HTML-like formatting
        return any(tag in message for tag in ["<b>", "<i>", "<u>", "<code>", "<pre>"])
