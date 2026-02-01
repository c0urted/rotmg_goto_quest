import time
import keyboard 
import config
from collections import deque
from core.win_api_manager import WinApiManager
from core.scraper import RealmScraper
from core.state_detector import StateDetector 

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def main():
    targets = config.TARGETS
    if isinstance(targets, str): targets = [targets]

    win_man = WinApiManager(config.WINDOW_TITLE)
    scraper = RealmScraper()
    detector = StateDetector(win_man)
    history = deque(maxlen=20)

    print("\n" + "="*50)
    log(f"ROTMG GOTO QUEST - HYBRID V1/V2")
    log(f"Targets: {targets}")
    log(f"Safety Check: {'ENABLED' if config.ENABLE_NEXUS_CHECK else 'DISABLED'}")
    print("="*50 + "\n")

    while True:
        try:
            # 1. Safety Check with clean UI
            if config.ENABLE_NEXUS_CHECK and not detector.is_in_nexus():
                print(f"\r[Status] 🟡 BUSY (In Dungeon) - Monitoring screen...          ", end="")
                time.sleep(3)
                continue

            # 2. Scanning Loop
            for target in targets:
                print(f"\r[Status] 🔍 Scanning for {target}... ", end="")
                
                events = scraper.find_events(target)
                print(f"Found {len(events)}.", end="")
                
                for event in events:
                    if event.uuid in history: continue
                    
                    print("\n" + "-"*30)
                    log(f"🚀 TARGET ACQUIRED: {event.name}")
                    log(f"🌐 SERVER/REALM: {event.server} - {event.realm}")
                    log(f"📍 IP: {event.ip}")
                    
                    if win_man.send_chat_command(f"/ip {event.ip}"):
                        history.append(event.uuid)
                        
                        log(f"⌛ Sleeping... ") #(Press Ctrl+M to skip)
                        time.sleep(15) # Wait for loading screen
                        
                        start_time = time.time()
                        while time.time() - start_time < config.RUN_TIMEOUT:
                            if keyboard.is_pressed('ctrl+m'):
                                log("⏭️ Manual Skip detected.")
                                break
                            if config.ENABLE_NEXUS_CHECK and detector.is_in_nexus():
                                log("🏠 Back in Nexus - resetting.")
                                break
                            time.sleep(1)
                        
                        print("-"*30)
                        break

            time.sleep(config.CHECK_INTERVAL)

        except KeyboardInterrupt:
            log("Shutting down...")
            break
        except Exception as e:
            log(f"⚠️ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()