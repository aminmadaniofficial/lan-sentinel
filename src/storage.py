import json
import logging
from typing import Dict, Set
from src.models import Device

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages loading and saving configuration files."""

    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_config(self) -> dict:
        """Loads configuration from the JSON file."""
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Configuration file not found at {self.config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in {self.config_path}")
            raise

class DeviceRegistry:
    """Tracks known devices and identifies unauthorized ones."""

    def __init__(self, known_devices_data: list):
        # Store known MAC addresses for O(1) lookup time
        self.known_macs: Dict[str, str] = {
            item["mac"].lower(): item["name"] for item in known_devices_data
        }

    def identify_new_devices(self, scanned_devices: list[Device]) -> list[Device]:
        """Compares scanned devices against the registry to find unrecognized ones."""
        unrecognized: list[Device] = []
        for device in scanned_devices:
            if device.mac not in self.known_macs:
                unrecognized.append(device)
            else:
                # Update device name from registry if it exists
                object.__setattr__(device, "name", self.known_macs[device.mac])
        return unrecognized