import logging
from src.models import Device

logger = logging.getLogger(__name__)

class AlertSystem:
    """Handles notification delivery when unauthorized devices are detected."""

    @staticmethod
    def notify_unauthorized_device(device: Device) -> None:
        """
        Triggers an alert. 
        Currently logs to console/file, but can be extended to Telegram/Email.
        """
        alert_message = (
            f"\n[ALERT] Unauthorized Device Detected!\n"
            f"IP Address: {device.ip}\n"
            f"MAC Address: {device.mac}\n"
            f"Please verify this device's access."
        )
        logger.warning(alert_message)