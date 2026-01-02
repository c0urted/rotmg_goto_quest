import time
import os
import config
from core.win_api_manager import WinApiManager
from core.scraper import RealmScraper

def main():
    target_mob = input("What are we farming today? (e.g., 'Oryx', 'Shatters'): ").strip()
    print(f"Target locked: {target_mob}")

    # Initialization
    win_man = WinApiManager(config.WINDOW_TITLE)
    scraper = RealmScraper()
    
    # Validation
    if not win_man.find_window():
        print("[Error] RotMGExalt window not found. Please open the game first.")
        return

    # Main Loop
    while True:
        print(f"\n[System] Scanning RealmStock API for {target_mob}...")
        
        # 1. Get IP (API Method)
        ip_list = scraper.find_ips_for_keyword(target_mob)
        
        if not ip_list:
            print("[System] No runs found. Retrying in 30 seconds...")
            time.sleep(30)
            continue

        # 2. Process Found IPs
        for ip in ip_list:
            print(f"[Action] Sending connect command to {ip}...")
            
            # This will work even if you are watching YouTube or playing another game
            success = win_man.send_chat_command(f"/ip {ip}")
            
            if success:
                print("[Action] Command sent. Waiting 5 minutes for run...")
                try:
                    time.sleep(300) 
                except KeyboardInterrupt:
                    print("[System] Wait cancelled.")
            else:
                print("[Error] Failed to send command (Window closed?).")

        print("[System] Cycle finished. Cooling down (2 minutes)...")
        time.sleep(120)

if __name__ == "__main__":
    main()