from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Device:
    """Represents a network device with its network attributes."""
    ip: str
    mac: str
    name: Optional[str] = "Unknown Device"

    def __post_init__(self):
        # Normalize MAC address to lowercase for consistent comparison
        object.__setattr__(self, "mac", self.mac.lower())