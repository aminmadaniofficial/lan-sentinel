import time
import sys
import logging
from rich.console import Console
from src.scanner import NetworkScanner
from src.storage import ConfigManager, DeviceRegistry
from src.notifier import TerminalUI

# Keep standard logs in a file, and use Rich UI for terminal
logging.basicConfig(
    level=logging.INFO,
    filename="network_sentinel.log",
    format="%(asctime)s [%(levelname)s] %(message)s"
)

console = Console()

def main():
    try:
        # Load configs
        config_manager = ConfigManager("config.json")
        config = config_manager.load_config()

        scanner = NetworkScanner(target_subnet=config["target_subnet"])
        registry = DeviceRegistry(known_devices_data=config["known_devices"])
        scan_interval = config.get("scan_interval_seconds", 60)

        console.print("[bold green]⚡ LAN Sentinel Security Service Active...[/bold green]")
        
        while True:
            # Showing a cool loading spinner during active scan
            with console.status("[bold yellow]Scanning network, please wait...", spinner="earth"):
                scanned_devices = scanner.scan()

            # Refresh names from registry
            unauthorized = registry.identify_new_devices(scanned_devices)

            # Draw Beautiful Device Dashboard
            TerminalUI.display_devices(scanned_devices)

            # Handle Alerts
            if unauthorized:
                for device in unauthorized:
                    TerminalUI.trigger_intrusion_alert(device)
            else:
                TerminalUI.display_secure_status()

            # Live countdown timer instead of static sleep
            for remaining in range(scan_interval, 0, -1):
                sys.stdout.write(f"\r\033[K[dim]⏳ Next scan in {remaining} seconds... (Ctrl+C to quit)[/dim]")
                sys.stdout.flush()
                time.sleep(1)
            console.print()  # Move to the next line after countdown finishes

    except KeyboardInterrupt:
        console.print("\n[bold orange3]⚠ Service stopped by operator.[/bold orange3]")
    except Exception as e:
        console.print(f"[bold red]Critical Error: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()