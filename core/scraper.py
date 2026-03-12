from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from core.models import RealmEvent
import time
import ctypes

try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except: pass

class RealmScraper:
    def __init__(self):
        self.driver = None
        self.launch_browser()

    def launch_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--window-size=1200,900")
        options.add_argument("--window-position=0,0")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://realmstock.com/pages/event-notifier")
        time.sleep(5)

    def get_ip_from_api(self, uuid):
        api_url = f"https://realmstock.network/Notifier/EventIp?email={config.RS_EMAIL}&id={uuid}"
        fetch_script = f"""
        var callback = arguments[arguments.length - 1];
        fetch('{api_url}').then(r => r.json()).then(d => callback(d)).catch(e => callback(null));
        """
        try:
            result = self.driver.execute_async_script(fetch_script)
            if result and result.get("success"):
                return result.get("value")
        except:
            return None

    def find_events(self, target_mob):
        found_events = []
        try:
            if "pages/event-notifier" not in self.driver.current_url:
                self.driver.get("https://realmstock.com/pages/event-notifier")
                time.sleep(3)

            # Your specific V1 XPath logic
            xpath = f"//h2[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{target_mob.lower()}')]/ancestor::div[contains(@class, 'realmstock-panel')]"
            panels = self.driver.find_elements(By.XPATH, xpath)

            for panel in panels:
                try:
                    uuid = panel.find_element(By.CSS_SELECTOR, "td.event-ip").get_attribute("id")
                    lines = panel.find_element(By.CLASS_NAME, "event-server").text.split("\n")
                    
                    event = RealmEvent(
                        uuid=uuid, 
                        name=target_mob, 
                        server=lines[0] if lines else "?", 
                        realm=lines[1] if len(lines) > 1 else "?"
                    )
                    
                    ip = self.get_ip_from_api(uuid)
                    if ip:
                        event.ip = ip
                        found_events.append(event)
                except: continue
        except Exception: pass
        return found_events
    
    def find_closed_realms(self):
        """
        Scans for 'Realm Closed' events and extracts the IP by finding 
        a 'Proxy' event (e.g. Red Demon) on the exact same Server/Realm.
        """
        found_events = []
        try:
            # Ensure we are on the right page
            if "pages/event-notifier" not in self.driver.current_url:
                self.driver.get("https://realmstock.com/pages/event-notifier")
                time.sleep(3)

            # 1. Grab ALL panels on the page efficiently
            # We use the class name we saw in your snippet logic
            all_panels = self.driver.find_elements(By.CLASS_NAME, "realmstock-panel")
            
            closed_candidates = [] # Stores: (server, realm)
            proxy_candidates = []  # Stores: {'server': s, 'realm': r, 'uuid': u}

            # 2. Parse everything in one pass
            for panel in all_panels:
                try:
                    # Extract Name, Server, Realm
                    name = panel.find_element(By.TAG_NAME, "h2").text.strip()
                    lines = panel.find_element(By.CLASS_NAME, "event-server").text.split("\n")
                    server = lines[0].strip()
                    realm = lines[1].strip() if len(lines) > 1 else "?"
                    
                    # Check if this is our target OR a proxy
                    if "Realm Closed" in name: 
                        closed_candidates.append((server, realm))
                    else:
                        # It's a normal event (Proxy). Save its UUID.
                        try:
                            # We grab the UUID from the IP button/field
                            uuid = panel.find_element(By.CSS_SELECTOR, "td.event-ip").get_attribute("id")
                            if uuid:
                                proxy_candidates.append({'server': server, 'realm': realm, 'uuid': uuid})
                        except: pass
                except: continue

            # 3. Match 'Closed' realms to 'Proxy' IPs
            for (c_server, c_realm) in closed_candidates:
                # Find the first proxy that matches this Server+Realm
                match = next((p for p in proxy_candidates if p['server'] == c_server and p['realm'] == c_realm), None)
                
                if match:
                    # Found a proxy! Hijack its UUID to get the IP.
                    ip = self.get_ip_from_api(match['uuid'])
                    
                    if ip:
                        # Create the event object
                        event = RealmEvent(
                            uuid=match['uuid'], # Use proxy UUID for tracking
                            name="Realm Closed (O3)",
                            server=c_server,
                            realm=c_realm
                        )
                        event.ip = ip
                        found_events.append(event)
                        
        except Exception as e:
            # print(f"Scraper Error: {e}") # Debug only
            pass
            
        return found_events