import logging
from typing import List
from scapy.all import ARP, Ether, srp
from src.models import Device
from src.vendor_resolver import VendorResolver

logger = logging.getLogger(__name__)

class NetworkScanner:
    """Handles network scanning and device discovery."""

    def __init__(self, target_subnet: str):
        self.target_subnet = target_subnet

    def scan(self) -> List[Device]:
        """Scans the subnet using ARP and resolves hardware vendors."""
        discovered_devices: List[Device] = []

        try:
            # Construct ARP Packet
            arp_request = ARP(pdst=self.target_subnet)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = broadcast / arp_request

            # Send/Receive packets
            answered_list, _ = srp(packet, timeout=2, verbose=False)

            for _, received in answered_list:
                mac = received.hwsrc
                vendor = VendorResolver.resolve(mac)
                
                device = Device(
                    ip=received.psrc, 
                    mac=mac, 
                    vendor=vendor
                )
                discovered_devices.append(device)

        except PermissionError:
            logger.error("Scan failed: Insufficient privileges (sudo required).")
        except Exception as e:
            logger.error(f"Scan error: {e}")

        return discovered_devices