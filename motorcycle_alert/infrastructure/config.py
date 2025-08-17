"""Configuration management for motorcycle alert system."""

import argparse
import os
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Config:
    """Application configuration."""

    telegram_api_key: str
    telegram_user_id: str
    api_base_url: str
    object_id: str
    check_interval: int
    status_file_path: str

    def __post_init__(self):
        """Validate configuration."""
        if not self.telegram_api_key:
            raise ValueError("TELEGRAM_API_KEY environment variable is required")
        if not self.telegram_user_id:
            raise ValueError("TELEGRAM_USER_ID environment variable is required")
        if not self.api_base_url:
            raise ValueError("API_BASE_URL environment variable is required")
        if not self.object_id:
            raise ValueError("OBJECT_ID environment variable is required")


def load_config() -> Config:
    """Load configuration from environment variables and arguments."""
    parser = argparse.ArgumentParser(
        description="Motorcycle Alert Configuration",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--check-interval",
        type=int,
        default=int(os.getenv("CHECK_INTERVAL", "60")),
        help="Check interval in seconds",
    )

    parser.add_argument(
        "--status-file",
        type=str,
        default=os.getenv("STATUS_FILE_PATH", "status.txt"),
        help="Path to status file",
    )

    args = parser.parse_args()

    return Config(
        telegram_api_key=os.getenv("TELEGRAM_API_KEY", ""),
        telegram_user_id=os.getenv("TELEGRAM_USER_ID", ""),
        api_base_url=os.getenv("API_BASE_URL", "https://servidormapa.com"),
        object_id=os.getenv("OBJECT_ID", ""),
        check_interval=args.check_interval,
        status_file_path=args.status_file,
    )


def get_api_headers() -> Dict[str, str]:
    """Get API headers from environment variables."""
    cookie = os.getenv("API_COOKIE", "")
    csrf_token = os.getenv("API_CSRF_TOKEN", "")

    if not cookie or not csrf_token:
        raise ValueError(
            "API_COOKIE and API_CSRF_TOKEN environment variables are required"
        )

    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Referer": f"{os.getenv('API_BASE_URL', 'https://servidormapa.com')}/objects",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "X-CSRF-TOKEN": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
    }
