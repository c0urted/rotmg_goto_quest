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