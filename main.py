import time
import keyboard  # pip install keyboard
import config
from collections import deque
from core.win_api_manager import WinApiManager
from core.state_detector import StateDetector
from core.scraper import RealmScraper

def smart_sleep(seconds):
    """
    Sleeps for 'seconds', but can be interrupted by pressing Ctrl+M.
    Returns True if skipped, False if finished normally.
    """
    print(f"[Wait] Sleeping for {seconds}s... Press 'Ctrl+M' to skip.")
    start_time = time.time()
    
    while time.time() - start_time < seconds:
        # Check if hotkey is pressed
        if keyboard.is_pressed('ctrl+m'):
            print("\n[System] Timer manually skipped!")
            # Wait a tiny bit so we don't trigger it twice instantly
            time.sleep(0.5) 
            return True
        time.sleep(0.1)
    
    return False

def main():
    target_mob = input("Farm Target: ").strip()
    
    win_man = WinApiManager(config.WINDOW_TITLE)
    scraper = RealmScraper()
    detector = StateDetector(win_man)
    
    history = deque(maxlen=20)

    print(f"\n[System] Tracking [{target_mob}]...")
    print(f"[System] Mode: Hybrid (Nexus Check + {config.RUN_TIMEOUT/60:.1f}min Timer)")

    if not win_man.find_window():
        print("[Error] Game window not found! Open RotMG first.")
        return

    while True:
        events = scraper.find_events(target_mob)
        
        for event in events:
            if event.uuid in history:
                continue

            # Safety Check
            is_safe = detector.is_in_safe_zone()
            if not is_safe:
                print(f"[System] New event ({event.server}), but you are in Dungeon.")
                time.sleep(5)
                continue 

            print(f"\n[>>>] NEW EVENT: {event}")
            
            if win_man.send_chat_command(f"/ip {event.ip}"):
                history.append(event.uuid)
                
                # SMART WAIT (Replaces simple sleep)
                smart_sleep(config.RUN_TIMEOUT)

                print("[System] Timer finished. Refreshing event list...")
                break 
            else:
                print("[Error] Failed to send command.")

        # Small sleep between API checks (can also use smart_sleep if you want to exit fast)
        time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()