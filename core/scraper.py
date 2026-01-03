from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from core.models import RealmEvent  # Import the model we just made

class RealmScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--window-size=1200,900") 
        
        print("[System] Initializing Chrome Driver...")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_ip_from_api(self, uuid):
        """
        Directly hits the RealmStock API using the user's email and event UUID.
        """
        email = config.RS_EMAIL
        api_url = f"https://realmstock.network/Notifier/EventIp?email={email}&id={uuid}"
        
        # Async script to fetch the data
        fetch_script = f"""
        var callback = arguments[arguments.length - 1];
        fetch('{api_url}')
            .then(response => response.json())
            .then(data => callback(data))
            .catch(err => callback({{error: err.toString()}}));
        """
        
        try:
            result = self.driver.execute_async_script(fetch_script)
            if result and result.get("success") is True:
                return result.get("value")
            else:
                return None
        except Exception as e:
            print(f"[API Error] Fetch failed: {e}")
            return None

    def find_events(self, target_mob):
        """
        Scrapes the HTML for event panels, then calls the API for IPs.
        Returns a list of RealmEvent objects.
        """
        found_events = []
        target_url = "https://realmstock.com/pages/event-notifier"
        
        # Ensure we are on the page
        if self.driver.current_url != target_url:
            self.driver.get(target_url)
            # Short sleep to let the table render (React/JS needs a moment)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "realmstock-panel"))
                )
            except:
                pass # Proceed anyway, maybe no events exist

        try:
            # 1. Find the Panel for the Mob
            # We look for the <h2> that contains the mob name, then go up to the main panel div
            xpath = f"//h2[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{target_mob.lower()}')]/ancestor::div[contains(@class, 'realmstock-panel')]"
            
            panels = self.driver.find_elements(By.XPATH, xpath)

            for panel in panels:
                try:
                    # 2. Extract UUID (It is the ID of the 'event-ip' td)
                    ip_td = panel.find_element(By.CSS_SELECTOR, "td.event-ip")
                    uuid = ip_td.get_attribute("id")
                    
                    # 3. Extract Server/Realm Info (Text parsing)
                    # Structure usually: "USSouthWest\nFrontier\n7/85"
                    server_div = panel.find_element(By.CLASS_NAME, "event-server")
                    lines = server_div.text.split("\n")
                    
                    s_name = lines[0] if len(lines) > 0 else "Unknown"
                    r_name = lines[1] if len(lines) > 1 else "Unknown"

                    # 4. Create Event Object
                    event = RealmEvent(
                        uuid=uuid,
                        name=target_mob,
                        server=s_name,
                        realm=r_name
                    )

                    # 5. Fetch IP from API
                    # Note: In the future, we can skip this call if we already have the UUID in history
                    # But for now, we just grab it to be safe.
                    ip = self.get_ip_from_api(uuid)
                    
                    if ip:
                        event.ip = ip
                        found_events.append(event)

                except Exception:
                    continue # Skip broken panels

        except Exception as e:
            # print(f"[Scraper Debug] Scan error: {e}") 
            pass

        return found_events