import logging
from typing import List
from scapy.all import ARP, Ether, srp
from src.models import Device

logger = logging.getLogger(__name__)

class NetworkScanner:
    """Handles low-level network scanning operations using ARP requests."""

    def __init__(self, target_subnet: str):
        self.target_subnet = target_subnet

    def scan(self) -> List[Device]:
        """
        Scans the target subnet using ARP requests.
        Returns a list of discovered Device objects.
        """
        logger.info(f"Initiating ARP scan on subnet: {self.target_subnet}")
        discovered_devices: List[Device] = []

        try:
            # Create an ARP request packet broadcasted to the network
            arp_request = ARP(pdst=self.target_subnet)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = broadcast / arp_request

            # Send and receive packets at Layer 2 (timeout set to 2 seconds)
            answered_list, _ = srp(packet, timeout=2, verbose=False)

            for sent, received in answered_list:
                device = Device(ip=received.psrc, mac=received.hwsrc)
                discovered_devices.append(device)

        except PermissionError:
            logger.error("Scan failed: Root privileges (sudo) are required to perform ARP scanning.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during the scan: {e}")

        return discovered_devices