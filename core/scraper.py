from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError, NewConnectionError
import config
from core.models import RealmEvent
import atexit
import psutil # Needed for cleanup
import time

class RealmScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        
        # 1. NUKE OLD PROCESSES ON START
        # This ensures we don't have 10 windows open if you restarted the bot 10 times.
        self.kill_zombies()
        
        # 2. Register cleanup for when we exit normally
        atexit.register(self.close_browser)
        
        self.launch_browser()

    def kill_zombies(self):
        """Finds and kills old ChromeDriver processes to prevent window pile-up."""
        print("[System] Checking for old browser sessions...")
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # We kill the DRIVER, which usually closes the browser window automatically
                if 'chromedriver' in proc.info['name'].lower():
                    proc.kill()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if killed:
            print("[System] Old sessions closed. Starting fresh.")
            time.sleep(1) # Give Windows a second to release the files

    def close_browser(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except:
                pass

    def launch_browser(self):
        self.close_browser()
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--log-level=3")
            options.add_argument("--window-size=1200,900")
            options.add_argument("--force-device-scale-factor=1")
            
            print("[System] Initializing Chrome Driver...")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f"[Critical] Failed to launch browser: {e}")

    def ensure_active(self):
        if self.driver is None:
            self.launch_browser()
            return False
        try:
            _ = self.driver.current_url
            return True
        except Exception:
            print("[Warning] Browser connection lost! Restarting Chrome...")
            self.launch_browser()
            return False

    def get_ip_from_api(self, uuid):
        email = config.RS_EMAIL
        api_url = f"https://realmstock.network/Notifier/EventIp?email={email}&id={uuid}"
        fetch_script = f"""
        var callback = arguments[arguments.length - 1];
        fetch('{api_url}').then(r => r.json()).then(d => callback(d)).catch(e => callback(null));
        """
        try:
            result = self.driver.execute_async_script(fetch_script)
            if result and result.get("success"): return result.get("value")
        except: return None

    def find_events(self, target_mob):
        if not self.ensure_active(): return []
        
        found_events = []
        target_url = "https://realmstock.com/pages/event-notifier"
        
        try:
            if target_url not in self.driver.current_url:
                self.driver.get(target_url)
                try: WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "realmstock-panel")))
                except: pass 

            xpath = f"//h2[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{target_mob.lower()}')]/ancestor::div[contains(@class, 'realmstock-panel')]"
            panels = self.driver.find_elements(By.XPATH, xpath)

            for panel in panels:
                try:
                    uuid = panel.find_element(By.CSS_SELECTOR, "td.event-ip").get_attribute("id")
                    lines = panel.find_element(By.CLASS_NAME, "event-server").text.split("\n")
                    event = RealmEvent(uuid=uuid, name=target_mob, server=lines[0] if lines else "?", realm=lines[1] if len(lines)>1 else "?")
                    
                    ip = self.get_ip_from_api(uuid)
                    if ip:
                        event.ip = ip
                        found_events.append(event)
                except: continue
        except: self.ensure_active()
        return found_events