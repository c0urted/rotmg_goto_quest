# RotMG Event Hopper (GoTo Quest)

A fully automated event finding and joining tool for **Realm of the Mad God Exalt**. 

This bot monitors RealmStock for specific events (e.g., "Oryx", "Shatters", "Event Gods"), extracts the server IP using direct API hooking (bypassing UI lag), and automatically connects your game client to the server using Windows API background injection.

## ⚡ Features

* **API-Level Scraping:** Bypasses the RealmStock UI refresh timer by hooking directly into the browser's `fetch` request to grab IPs instantly via UUID.
* **Background Input:** Uses `pywin32` and Flash Focus to inject `/ip` commands into the game window, allowing you to multitask or watch videos while it works.
* **Smart Run Monitoring:** Uses OpenCV (`nexus_pattern.png`) to detect when you leave the Nexus (start run) and when you return (end run), eliminating the need for hardcoded timers.
* **Blind Mode:** If image detection fails, it falls back to a timer-based system automatically.
* **Secure Config:** Uses `.env` variables to keep your credentials safe from version control.

## 📋 Prerequisites

* Windows 10/11
* Python 3.10+
* Google Chrome (installed)
* **RealmStock Access:** You must have a valid email and Order ID (OTP) for RealmStock's notifier.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/c0urted/rotmg_goto_quest.git](https://github.com/c0urted/rotmg_goto_quest.git)
    cd rotmg_goto_quest
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If you don't have a requirements.txt yet, install these manually):*
    ```bash
    pip install selenium webdriver-manager pywin32 python-dotenv pyperclip pyautogui opencv-python pillow
    ```

## ⚙️ Configuration

### 1. Environment Variables
Create a file named `.env` in the root directory. Add your details:

```ini
# .env
WINDOW_TITLE=RotMGExalt
RS_EMAIL=your_email@gmail.com
RS_STATIC_OTP=123456