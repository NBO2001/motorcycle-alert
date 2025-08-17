"""Tests for domain models."""

import pytest

from motorcycle_alert.domain.models import AlertMessage, MotorcycleStatus


class TestMotorcycleStatus:
    """Test cases for MotorcycleStatus domain model."""

    def test_create_valid_status(self):
        """Test creating a valid motorcycle status."""
        status = MotorcycleStatus(
            icon_color="green", alimentation="12V", blocked=False, ignition="on"
        )

        assert status.icon_color == "green"
        assert status.alimentation == "12V"
        assert status.blocked is False
        assert status.ignition == "on"

    def test_invalid_empty_icon_color(self):
        """Test that empty icon color raises ValueError."""
        with pytest.raises(ValueError, match="Icon color cannot be empty"):
            MotorcycleStatus(
                icon_color="", alimentation="12V", blocked=False, ignition="on"
            )

    def test_invalid_blocked_type(self):
        """Test that non-boolean blocked value raises ValueError."""
        with pytest.raises(ValueError, match="Blocked status must be a boolean"):
            MotorcycleStatus(
                icon_color="green",
                alimentation="12V",
                blocked="false",  # Should be boolean
                ignition="on",
            )

    def test_status_equality(self):
        """Test that status objects with same values are equal."""
        status1 = MotorcycleStatus(
            icon_color="green", alimentation="12V", blocked=False, ignition="on"
        )

        status2 = MotorcycleStatus(
            icon_color="green", alimentation="12V", blocked=False, ignition="on"
        )

        assert status1 == status2

    def test_status_inequality(self):
        """Test that status objects with different values are not equal."""
        status1 = MotorcycleStatus(
            icon_color="green", alimentation="12V", blocked=False, ignition="on"
        )

        status2 = MotorcycleStatus(
            icon_color="red", alimentation="12V", blocked=False, ignition="on"
        )

        assert status1 != status2


class TestAlertMessage:
    """Test cases for AlertMessage domain model."""

    def test_format_message(self):
        """Test message formatting."""
        status = MotorcycleStatus(
            icon_color="green",
            alimentation="12V",
            blocked=False,
            ignition="on",
            time="2024-01-01 12:00:00",
            stop_duration="5 min",
            speed="0 km/h",
        )

        alert = AlertMessage(status=status, timestamp="2024-01-01 12:05:00")

        message = alert.format_message()

        assert "🏍️ Motorcycle Status Update:" in message
        assert "Icon Color: green" in message
        assert "Time: 2024-01-01 12:00:00" in message
        assert "Alimentation: 12V" in message
        assert "Blocked: No" in message
        assert "Ignition: on" in message
        assert "Alert Time: 2024-01-01 12:05:00" in message

    def test_format_message_with_additional_sensors(self):
        """Test message formatting with additional sensors."""
        status = MotorcycleStatus(
            icon_color="green",
            alimentation="12V",
            blocked=False,
            ignition="on",
            additional_sensors={"temperature": "25°C", "fuel": "80%"},
        )

        alert = AlertMessage(status=status, timestamp="2024-01-01 12:05:00")

        message = alert.format_message()

        assert "Additional Sensors:" in message
        assert "temperature" in message
        assert "fuel" in message
