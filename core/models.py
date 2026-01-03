from dataclasses import dataclass
from datetime import datetime

@dataclass
class RealmEvent:
    uuid: str          # Unique ID from RealmStock (Best for tracking history)
    name: str          # e.g. "Grand Sphinx"
    server: str        # e.g. "USWest"
    realm: str         # e.g. "Medusa"
    ip: str = None     # We fill this in later via API
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        return f"[{self.timestamp}] {self.name} | {self.server}/{self.realm} | {self.ip}"