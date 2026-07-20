import time
import sys
import logging
from src.scanner import NetworkScanner
from src.storage import ConfigManager, DeviceRegistry
from src.notifier import AlertSystem

# Configure logging to write to console with standard format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("LAN_Sentinel")

def main():
    try:
        # Load configurations
        config_manager = ConfigManager("config.json")
        config = config_manager.load_config()

        # Initialize core systems
        scanner = NetworkScanner(target_subnet=config["target_subnet"])
        registry = DeviceRegistry(known_devices_data=config["known_devices"])
        scan_interval = config.get("scan_interval_seconds", 60)

        logger.info("LAN Sentinel service has started successfully.")
        
        while True:
            # Perform scan
            scanned_devices = scanner.scan()
            logger.info(f"Scan complete. Found {len(scanned_devices)} active devices.")

            # Identify strangers
            unauthorized = registry.identify_new_devices(scanned_devices)
            
            if unauthorized:
                for device in unauthorized:
                    AlertSystem.notify_unauthorized_device(device)
            else:
                logger.info("No unauthorized devices detected on the network.")

            # Wait before next cycle
            time.sleep(scan_interval)

    except KeyboardInterrupt:
        logger.info("Service terminated gracefully by user.")
    except Exception as e:
        logger.critical(f"Service crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()