from typing import Dict

class VendorResolver:
    """Resolves MAC address to hardware manufacturer using local OUI mapping."""
    
    # Common OUI (Organizationally Unique Identifier) mapping
    _OUI_DATABASE: Dict[str, str] = {
        "00:15:5d": "Microsoft Corporation (Hyper-V)",
        "00:0c:29": "VMware, Inc.",
        "3c:5a:37": "Apple, Inc.",
        "f4:f5:e8": "Google, Inc.",
        "00:e0:4c": "Realtek Semiconductor",
        "b4:b5:b6": "Samsung Electronics",
        "00:1a:11": "Google Fiber",
        "00:50:56": "VMware",
        "00:1c:42": "Parallels",
    }

    @classmethod
    def resolve(cls, mac: str) -> str:
        """Extracts OUI from MAC address and returns the vendor name."""
        # Standardize format (e.g., 00:11:22)
        oui = mac.lower()[:8]
        return cls._OUI_DATABASE.get(oui, "Unknown Vendor")