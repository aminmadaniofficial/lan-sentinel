from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.models import Device

# Professional terminal output helper
console = Console()

class TerminalUI:
    """Handles rendering clean, colored dashboards and alerts in the terminal."""

    @staticmethod
    def display_devices(devices: list[Device]) -> None:
        """Renders a beautiful table of all active devices."""
        table = Table(title="[bold blue]📡 Active Network Devices[/bold blue]", show_header=True, header_style="bold magenta")
        table.add_column("IP Address", style="cyan", justify="left")
        table.add_column("MAC Address", style="green", justify="center")
        table.add_column("Device Name", style="yellow", justify="left")
        table.add_column("Manufacturer (Vendor)", style="blue", justify="left")

        for dev in devices:
            table.add_row(dev.ip, dev.mac, dev.name, dev.vendor)

        console.print(table)

    @staticmethod
    def trigger_intrusion_alert(device: Device) -> None:
        """Displays a prominent red panel indicating an unauthorized device intrusion."""
        alert_content = (
            f"[bold]An unrecognized device has joined your LAN![/bold]\n\n"
            f"• [bold red]IP Address:[/bold red]  {device.ip}\n"
            f"• [bold red]MAC Address:[/bold red] {device.mac}\n"
            f"• [bold red]Vendor:[/bold red]      {device.vendor}"
        )
        alert_panel = Panel(
            alert_content,
            title="[bold blink white on red]⚠️ SECURITY INTRUSION DETECTED[/bold blink white on red]",
            border_style="red",
            expand=False
        )
        console.print(alert_panel)

    @staticmethod
    def display_secure_status() -> None:
        """Displays a neat green confirmation message."""
        console.print("[bold green]✔ Network secure. No intruders detected.[/bold green]")