"""Integration tests for the motorcycle alert system."""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from motorcycle_alert.domain.models import MotorcycleStatus
from motorcycle_alert.infrastructure.config import Config, load_config
from motorcycle_alert.infrastructure.storage import FileStatusStorage


class TestConfiguration:
    """Test configuration loading and validation."""

    def test_load_config_with_environment_variables(self):
        """Test loading configuration from environment variables."""
        with patch.dict(
            os.environ,
            {
                "TELEGRAM_API_KEY": "test_key",
                "TELEGRAM_USER_ID": "12345",
                "API_BASE_URL": "https://test.com",
                "OBJECT_ID": "999",
                "API_COOKIE": "test_cookie",
                "API_CSRF_TOKEN": "test_token",
            },
        ):
            # Mock sys.argv to avoid argument parsing issues
            with patch("sys.argv", ["test"]):
                config = load_config()

            assert config.telegram_api_key == "test_key"
            assert config.telegram_user_id == "12345"
            assert config.api_base_url == "https://test.com"
            assert config.object_id == "999"

    def test_config_validation_missing_telegram_key(self):
        """Test that missing Telegram API key raises error."""
        with pytest.raises(ValueError, match="TELEGRAM_API_KEY"):
            Config(
                telegram_api_key="",
                telegram_user_id="12345",
                api_base_url="https://test.com",
                object_id="999",
                check_interval=60,
                status_file_path="status.txt",
            )


class TestFileStatusStorage:
    """Test file-based status storage."""

    def test_save_and_load_status(self):
        """Test saving and loading status from file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            storage = FileStatusStorage(f.name)

            status = MotorcycleStatus(
                icon_color="green",
                alimentation="12V",
                blocked=False,
                ignition="on",
            )

            storage.save_status(status)
            loaded_status = storage.load_last_status()

            assert loaded_status == status

        # Clean up
        os.unlink(f.name)

    def test_load_status_file_not_exists(self):
        """Test loading status when file doesn't exist."""
        storage = FileStatusStorage("/nonexistent/file.txt")
        result = storage.load_last_status()
        assert result is None
