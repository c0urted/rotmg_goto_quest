import time
import keyboard  # pip install keyboard
import config
from datetime import datetime
from collections import deque
from core.win_api_manager import WinApiManager
from core.state_detector import StateDetector
from core.scraper import RealmScraper
# from core.logger import Logger  # Uncomment if you created the logger file

def get_time():
    """Returns current time string for logging."""
    return datetime.now().strftime("%H:%M:%S")

def log(message):
    """Helper to print with timestamp."""
    print(f"[{get_time()}] {message}")

def smart_sleep(seconds):
    """
    Sleeps for 'seconds', but can be interrupted by pressing Ctrl+M.
    Returns True if skipped, False if finished normally.
    """
    log(f"[Wait] Sleeping for {seconds}s... Press 'Ctrl+M' to skip.")
    start_time = time.time()
    
    while time.time() - start_time < seconds:
        if keyboard.is_pressed('ctrl+m'):
            print("") # Newline for cleanliness
            log("[System] Timer manually skipped!")
            time.sleep(0.5) 
            return True
        time.sleep(0.1)
    
    return False

def main():
    target_mob = input("Farm Target: ").strip()
    
    win_man = WinApiManager(config.WINDOW_TITLE)
    scraper = RealmScraper()
    detector = StateDetector(win_man)
    # logger = Logger() # Uncomment if using logger
    
    history = deque(maxlen=20)

    log(f"[System] Tracking [{target_mob}]...")
    log(f"[System] Mode: Hybrid (Nexus Check + {config.RUN_TIMEOUT/60:.1f}min Timer)")

    if not win_man.find_window():
        log("[Error] Game window not found! Open RotMG first.")
        return

    while True:
        events = scraper.find_events(target_mob)
        
        for event in events:
            if event.uuid in history:
                continue

            # Safety Check
            if not detector.is_in_safe_zone():
                log(f"[System] New event found ({event.server}), but you are in Dungeon. Waiting...")
                time.sleep(5)
                continue 

            print("") # Spacer line
            log(f"[>>>] NEW EVENT: {event.name} | {event.server} | {event.ip}")
            
            if win_man.send_chat_command(f"/ip {event.ip}"):
                history.append(event.uuid)
                
                # Optional: Log to file
                # logger.log_run(event, status="Joined")

                # SMART WAIT
                smart_sleep(config.RUN_TIMEOUT)

                log("[System] Timer finished. Refreshing event list...")
                break 
            else:
                log("[Error] Failed to send command.")

        # Small sleep between API checks
        time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()