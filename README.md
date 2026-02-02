# RotMG Event Hopper (V1-V2 Hybrid) 🚀

A high-speed automation tool for **Realm of the Mad God Exalt**. This bot scrapes event data directly from RealmStock and injects `/ip` connection commands into the game client. 

Designed for 24/7 background operation with integrated safety checks to prevent joining runs while currently in a dungeon.

---

## Key Features

* **Low-Level Win32 Injection:** Uses `SendMessage` with **Hardware Scan Code spoofing** (0x1C) to bypass Unity's input filters. Operates via the Windows Message Queue, allowing background execution.
* **Input State Purging:** Features an automated focus-reset sequence (using `WM_ACTIVATE` and hardware `KEYUP` pulses) to maintain client stability.
* **Web Scraper:** Pulls event IPs via realmstock.
* **Nexus Safety Check:** Uses pixel-detection to verify you are in the Nexus before attempting to jump servers.
* **Server Blacklist:** Optional filtering in `config.py` to automatically skip laggy or antihack filled servers.
* **DPI Aware:** Integrated `ctypes` support to handle Windows display scaling automatically for pixel-perfect accuracy.
---
![Proof of it working in Visual studio code](images/image.png)

Proof of it working in Visual studio code ^^
## Setup

### Prerequisites
* Python 3.10+
* Google Chrome
* A [RealmStock](https://realmstock.com) account (Requires valid Email + Static OTP/Order ID).

### Installation

1.  **Clone & Navigate:**
    ```bash
    git clone [https://github.com/c0urted/rotmg_goto_quest.git](https://github.com/c0urted/rotmg_goto_quest.git)
    cd rotmg_goto_quest
    ```
    or download as a .zip and extract.

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup:**
    Create a `.env` file in the root directory:
    ```ini
    RS_EMAIL=your_email@gmail.com
    RS_STATIC_OTP=your_static_otp
    WINDOW_TITLE=RotMGExalt
    ```

---

## 🔍 Nexus Detection Calibration

The bot requires calibration to distinguish between the Nexus and a dungeon.

1.  Stand in the **Nexus**.
2.  Run `calibration.py`.
3.  Hover over static UI elements top right (Gold icon, Fame icon, and Shop button) and press **`Ctrl + B`**.
4.  Capture **3-5 points** and press **`Ctrl + S`** to save.

**Now you have your nexus detection setup and just need to run main.py**
----


### How it Works
The bot checks your saved coordinates. If a majority of the pixels match (e.g., 3 out of 4), the bot stays in **Safe Mode**. If you enter a portal, the UI changes, the pixels no longer match, and the bot enters **Busy Mode** automatically.

---

## 💻 Running the Bot (VS Code & Admin)

To send the `/ip` command to the game, the bot must have permission to interact with the RotMG window.

1.  **Open VS Code or Command Prompt as Administrator**: 
2.  **Navigate to the folder**
    -  ```cd C:\Users\username\Desktop\rotmg_goto_quest```
3.  **Run the Script**:
    ```
    python main.py
    ```
*Note: If you do not run as Admin, the bot will scan successfully but the game will ignore the typed commands.*

---

## 🎮 Usage & Controls

1.  Launch RotMG Exalt and ensure you are in the Nexus.
2.  Update your `TARGETS` in `config.py` (e.g., `TARGETS = ["Cube God", "Lost Sentry"]`).
  `server blacklist coming soon`
3.  **Controls**:
    - **`Ctrl + M`**: Force skip the current sleep timer.
    - **`Ctrl + C`**: Kill the bot and all associated browser sessions.

---


## Project Structure

* `main.py`: Primary loop and polished terminal interface.
* `calibration.py`: Pixel selector for Nexus detection.
* `core/scraper.py`: Selenium-based event scraper (V1 Logic).
* `core/state_detector.py`: Pixel-matching safety engine.
* `core/win_api_manager.py`: Handles background command injection.
* `pixel_config.json`: Stores your calibrated UI data.

---


## ⚠️ Disclaimer
This tool is for educational purposes. Automated event hopping is against ToS and we don't break the ToS! Use at your own risk.