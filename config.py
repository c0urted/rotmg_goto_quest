import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# --- SENSITIVE DATA (Loaded from .env) ---
# Defaults are provided as a fallback or empty string if missing
WINDOW_TITLE = os.getenv("WINDOW_TITLE", "RotMGExalt")
RS_EMAIL = os.getenv("RS_EMAIL")
RS_STATIC_OTP = os.getenv("RS_STATIC_OTP")

# Validation to ensure .env is set up correctly
if not RS_EMAIL:
    raise ValueError("Missing RS_EMAIL in .env file! Please set it up.")

# --- STATIC SETTINGS ---
# Realmstock URLs
REALMSTOCK_URL = "https://realmstock.com/pages/event-notifier"
REALMSTOCK_LOGIN_URL = "https://realmstock.com/account/login"
# --- BOT CONFIGURATION ---

# 2. Safety Settings
# Set to True to prevent joining runs while you are already in a dungeon.
# Set to False to disable pixel checking (Blind Mode).
ENABLE_NEXUS_CHECK = True

# 3. Timers
# How long (in seconds) to wait inside a dungeon before leaving.
# The bot will skip this automatically if it sees you Nexus early.
RUN_TIMEOUT = 1200  # Default: 20 mins

# How often (seconds) to check RealmStock for new events.
CHECK_INTERVAL = 2.0

# 4. Targets
# List the exact names of events you want to farm.
TARGETS = [
### SHATTERS
    # "Avatar of the Forgotten King",
    # "Flying Behemoth"
### SPEC PEN
    # "Skeletal Centipede"
### NEST
#    "Corrupted Bramblethorn",
#    "Killer Bee Nest"
### FUNGALS
#    "Ancient Kaiju",
#    "Adult Baneserpent"
### LOST HALLS
    # "Bloodroot Heart",
    # "Ravenous Rot",
    # "Lost Sentry"
### KOGBOLD
    "Aerial Warship",
    "Kogbold Expedition Engine"

### WORLD EVENT ITEMS
   # "Keyper"
   # "Jotunn"
## JUGG HELM 
   # "Grand Sphinx",
   # "Crab Sovereign",
   # "Sigma Werewolf"
## CDIRK
   # "Cube God",
   # "Astral Rift"

   # "Grand Sphinx",
   # "Hermit God"
]

# 5. Additional Settings | legacy from V1
# 5. O3 Hunting Mode
# Set to True to ignore TARGETS and exclusively hunt for "Realm Closed" events
# by finding proxy events on the same server to get the IP.
HUNT_CLOSED_REALMS = False
