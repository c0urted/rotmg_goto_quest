# 🤖 RotMG Event Auto-Joiner (GoTo Quest)

This is a bot for **Realm of the Mad God Exalt**. It automatically finds events (like "Oryx", "Shatters", "Kaiju") using RealmStock and **joins the server for you** so you don't have to type IPs manually.

**It works in the background.** You can watch YouTube or play other games while it runs.

---

## ⚠️ READ THIS FIRST

1.  **Run as Administrator:** This bot **WILL NOT WORK** if you do not run it as Administrator. Windows prevents programs from typing into games unless they have Admin permissions.
2.  **RealmStock Account:** You need a valid email and Order ID (OTP) from [RealmStock](https://realmstock.com) to use this.
3.  **Use at your own risk:** Automating games can be against Terms of Service.

---

## STEP 1: Install Python (The Engine)

You need Python to run this script.

1.  Go to [python.org/downloads](https://www.python.org/downloads/).
2.  Click the big yellow **"Download Python"** button.
3.  **CRITICAL STEP:** When the installer opens, check the box at the bottom that says **"Add Python to PATH"**.
    * **
    * If you miss this, the bot won't work.
4.  Click **Install Now** and wait for it to finish.

---

## STEP 2: Download & Setup the Bot

1.  **Download:** Click the green **Code** button at the top of this page -> **Download ZIP**.
2.  **Extract:** Open the ZIP file and drag the folder out to your Desktop.
3.  **Open the Folder:** Go inside the folder. You should see files like `main.py` and `config.py`.

---

## STEP 3: Install the "Helpers" (Libraries)

The bot needs some extra tools to control Chrome and type keys.

1.  Inside the bot folder, right-click on empty space and select **"Open in Terminal"** (or "Open PowerShell window here").
    * *If you don't see that option: Type `cmd` in the address bar at the top of the folder window and hit Enter.*
2.  A black window will pop up. Paste this command and hit Enter:
    ```bash
    pip install -r requirements.txt
    ```
3.  Wait for all the text to stop scrolling. If you see "Successfully installed", you are good.

---

## STEP 4: Enter Your Settings

We need to tell the bot your email and password safely.

1.  Look for a file named `.env` in the folder.
    * *Don't see it? Create a new text file, name it `.env` (yes, just `.env`, no `.txt` at the end).*
2.  Open `.env` with Notepad.
3.  Paste this inside and fill in your info:

    ```ini
    # Your RealmStock purchase email
    RS_EMAIL=myemail@gmail.com
    
    # Your Order ID (Check your email from RealmStock)
    RS_STATIC_OTP=123456
    
    # Leave this alone unless you renamed your game window
    WINDOW_TITLE=RotMGExalt
    ```
4.  **Save the file** (File -> Save).

---

## STEP 5: (Optional) Smart Detection *NOT ADDED YET*

The bot can "see" when you finish a dungeon so it knows when to start searching again.

1.  Go to the Nexus in-game.
2.  Take a screenshot (Windows Key + Shift + S) of something static, like the **Vault Portal** or the **Fountains**.
    * *Do NOT capture players or pets moving around.*
3.  Save the image as `nexus_pattern.png` inside the bot folder.
4.  *If you skip this, the bot will just wait 5 minutes per run automatically.*

---

## 🚀 STEP 6: HOW TO RUN IT

1.  **Open RotMG Exalt** and sit in the Nexus.
2.  Go to your bot folder.
3.  **Right-Click** inside the folder (on empty white space).
4.  Select **"Open in Terminal"** (or PowerShell/CMD).
    * *Note: If you are launching from VS Code, right-click VS Code and select "Run as Administrator".*
5.  Type this command and hit Enter:
    ```bash
    python main.py
    ```
6.  The bot will ask: `What are we farming today?`
    * Type: `Oryx` (or `Shatters`, `Nest`, etc).
7.  **Hit Enter.**

**That's it!** A minimized Chrome window will open. The bot will scan for the event, and as soon as one pops up, it will type the `/ip` command into your game automatically.

---

## ❓ Troubleshooting (Help, it broke!)

**Error: "Access is denied"**
* **Fix:** You didn't run the terminal as Administrator. Close it, search for "Command Prompt" in your Start Menu, right-click -> **Run as Administrator**, navigate to the folder, and try again.

**Error: "Module not found: selenium" (or others)**
* **Fix:** You skipped Step 3. Run `pip install -r requirements.txt` again.

**The bot says "Command sent" but nothing happened in game**
* **Fix:** Your game window might be minimized to the taskbar. Open the game window so it's on screen, then you can put other windows (like Chrome/Discord) over it. It just can't be minimized.

**The bot crashes immediately**
* **Fix:** Check your `.env` file. Did you save it? Did you put your correct email?