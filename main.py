import time
import os
import config
from collections import deque
from core.win_api_manager import WinApiManager
from core.state_detector import StateDetector
from core.scraper import RealmScraper

def main():
    target_mob = input("Farm Target: ").strip()
    
    win_man = WinApiManager(config.WINDOW_TITLE)
    detector = StateDetector()
    scraper = RealmScraper()
    
    # HISTORY: Store UUIDs so we never re-join the same event ID
    history = deque(maxlen=20)

    print(f"\n[System] tracking [{target_mob}]...")

    while True:
        # 1. Scrape Events (Returns list of RealmEvent objects)
        events = scraper.find_events(target_mob)
        
        # 2. Filter Process
        for event in events:
            # SKIP if we already did this UUID
            if event.uuid in history:
                continue
            
            # SKIP if we are currently in a dungeon (Safety check)
            if not detector.is_in_nexus():
                print("[System] Waiting to return to Nexus...")
                time.sleep(2)
                continue

            # NEW EVENT FOUND
            print(f"\n[>>>] NEW EVENT: {event}") # Uses the nice string format we made
            
            # Join
            if win_man.send_chat_command(f"/ip {event.ip}"):
                history.append(event.uuid)
                
                # Wait loop
                print("[State] Waiting for departure...")
                # (Insert your wait logic here)
                time.sleep(5) 
                
                # We break to refresh the list, ensuring we don't process stale events
                break 
        
        time.sleep(2) # Fast polling since we optimized the image detection

if __name__ == "__main__":
    main()