"""Domain models for motorcycle alert system."""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class MotorcycleStatus:
    """Domain model representing motorcycle status."""

    icon_color: str
    alimentation: str
    blocked: bool
    ignition: str
    time: Optional[str] = None
    stop_duration: Optional[str] = None
    speed: Optional[str] = None
    additional_sensors: Optional[Dict[str, str]] = None

    def __post_init__(self):
        """Validate motorcycle status data."""
        if not self.icon_color:
            raise ValueError("Icon color cannot be empty")

        if not isinstance(self.blocked, bool):
            raise ValueError("Blocked status must be a boolean")

    def __eq__(self, other):
        """Check equality of two MotorcycleStatus instances."""
        if not isinstance(other, MotorcycleStatus):
            return NotImplemented
        return (
            self.icon_color == other.icon_color
            and self.alimentation == other.alimentation
            and self.blocked == other.blocked
            and self.ignition == other.ignition
        )

@dataclass(frozen=True)
class AlertMessage:
    """Domain model for alert messages."""

    status: MotorcycleStatus
    timestamp: str

    def format_message(self) -> str:
        """Format the alert message for sending."""
        sensors_info = ""
        if self.status.additional_sensors:
            sensors_info = f"\n- Additional Sensors: {self.status.additional_sensors}"

        return f"""🏍️ Motorcycle Status Update:
- Icon Color: {self.status.icon_color}
- Time: {self.status.time or 'N/A'}
- Stop Duration: {self.status.stop_duration or 'N/A'}
- Speed: {self.status.speed or 'N/A'}
- Alimentation: {self.status.alimentation}
- Blocked: {'Yes' if self.status.blocked else 'No'}
- Ignition: {self.status.ignition}{sensors_info}

📅 Alert Time: {self.timestamp}"""
