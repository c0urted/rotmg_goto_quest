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

# Timings
CHECK_INTERVAL = 2.0  # How often to check for runs

# Legacy Pixel Check (Optional/Legacy)
NEXUS_ICON_POS = (1800, 200) 
NEXUS_ICON_COLOR = (255, 215, 0)