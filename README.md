# RotMG Event Hopper

A lightweight automation tool for **Realm of the Mad God Exalt** and Xclient (rip Connect to Quest). Scrapes event data from RealmStock and automatically connects your client to servers hosting specific events (Oryx, Shatters, Nest, etc.).

Designed to run in the background with minimal interference.

## Features

* **API Hooking:** Bypasses the frontend UI refresh to grab IPs instantly via UUID.
* **Background Injection:** Uses `pywin32` and clipboard injection to enter `/ip` commands without stealing mouse focus for long periods.
* **Session Management:**
    * **Single Window:** Reuses a single Chrome instance to prevent RAM bloat.
    * **Auto-Cleanup:** Kills zombie Chrome processes and drivers on exit.
    * **Smart Wait:** Custom sleep logic allows you to skip timers instantly with `Ctrl+M`.
* **Hybrid Safety:** Checks if your character is safely in the Nexus before attempting to join a new run (preventing disconnects/deaths in dungeons). **NOT ADDED YET**

## Setup

### Prerequisites
* Python 3.10+
* Google Chrome
* A [RealmStock](https://realmstock.com) account with a valid Order ID (OTP).

### Installation

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/c0urted/rotmg_goto_quest.git](https://github.com/c0urted/rotmg_goto_quest.git)
    cd rotmg_goto_quest
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a file named `.env` in the root directory and add your credentials:
    ```ini
    RS_EMAIL=your_email@gmail.com
    RS_STATIC_OTP=123456
    WINDOW_TITLE=RotMGExalt
    ```

4.  **Optional: Safety Images**
    For the safety check to work, take a screenshot of a static object in the Nexus (like the Vault portal or a fountain) and save it as `nexus_portal.png` in the root folder.
    * *If skipped, the bot runs in "Blind Mode" (timer only).*

## Usage

1.  Open RotMG Exalt and stay in the Nexus.
2.  Run the script **as Administrator** (required to send input to the game):
    ```bash
    python main.py
    ```
3.  Enter the event name when prompted (e.g., `Adult Baneserpent`, `Ancient Kaiju`, `The Nest`, `Elder Ent Ancient` etc).

### Controls
* **`Ctrl + M`**: Skip the current wait timer and search for the next run immediately.
* **`Ctrl + C`**: Stop the bot and close all browser sessions.

## Configuration (`config.py`)

Adjust `RUN_TIMEOUT` in `config.py` to match the dungeon you are farming.

```python
# Example Timers (Seconds)
# Nest (Public): 920
# Fungal + Crystal: 1820
RUN_TIMEOUT = 920