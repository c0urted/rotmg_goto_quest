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
    "Grand Sphinx",
    "Crab Sovereign",
    "Sigma Werewolf"

   # "Grand Sphinx",
   # "Hermit God"
]

# 5. Additional Settings | legacy from V1
# HOW LONG TO WAIT AFTER JOINING A RUN
# Time in seconds (1200 seconds = 20 minutes)
RUN_TO_QUEST = 180 # Time to run to quest after server swap
RUN_TIMEOUT = RUN_TO_QUEST +  1200
# time key
# 200s for tp cooldown and running to quest
# +
# Fungal Cavern: 15 minutes | 900s
# Crystalline Cavern: 12 minutes | 720s
# Nest: 8-12 minutes
# MBC: 15 minutes? | 900s