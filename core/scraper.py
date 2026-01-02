from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time
import json

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
        Bypasses the entire UI/Button/Alert flow.
        """
        email = config.RS_EMAIL
        api_url = f"https://realmstock.network/Notifier/EventIp?email={email}&id={uuid}"
        
        print(f"[API] Fetching: {api_url}")

        # specific JS wrapper to handle the Fetch Promise
        fetch_script = f"""
        var callback = arguments[arguments.length - 1];
        fetch('{api_url}')
            .then(response => response.json())
            .then(data => callback(data))
            .catch(err => callback({{error: err.toString()}}));
        """
        
        try:
            # execute_async_script waits for the fetch to complete and returns the data
            result = self.driver.execute_async_script(fetch_script)
            
            # Parse the JSON response: {"success":true,"value":"54.170.71.231"}
            if result:
                if result.get("success") is True:
                    return result.get("value")
                else:
                    print(f"[API Error] Server rejected request: {result}")
                    return None
            else:
                print("[API Error] Empty response from API.")
                return None

        except Exception as e:
            print(f"[API Critical] Fetch execution failed: {e}")
            return None

    def find_ips_for_keyword(self, target_mob):
        found_ips = []
        target_url = "https://realmstock.com/pages/event-notifier"
        
        # Load the page once to establish session/cookies
        if self.driver.current_url != target_url:
            self.driver.get(target_url)
            time.sleep(4) 

        try:
            # 1. FIND THE UUID (The ID of the event)
            # We don't care about buttons or stale elements anymore. Just get the ID.
            print(f"[DEBUG] Scanning for '{target_mob}' UUID...")
            
            xpath = f"//h2[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{target_mob.lower()}')]/ancestor::div[contains(@class, 'realmstock-panel')]"
            
            try:
                # Find the panel
                panel = self.driver.find_element(By.XPATH, xpath)
                
                # Find the 'td' that holds the UUID
                # The HTML structure you showed earlier: <td class="event-ip" id="UUID">
                ip_td = panel.find_element(By.CSS_SELECTOR, "td.event-ip")
                event_uuid = ip_td.get_attribute("id")
                
                print(f"[MATCH] Found Event UUID: {event_uuid}")
                
            except Exception:
                print(f"[DEBUG] No events found for '{target_mob}'.")
                return found_ips

            # 2. CALL API DIRECTLY
            # We have the UUID, we have the email. We don't need to click anything.
            ip = self.get_ip_from_api(event_uuid)
            
            if ip:
                print(f"[SUCCESS] API returned IP: {ip}")
                found_ips.append(ip)
                
                # Optional: Refresh page to keep session fresh, though not strictly needed for API calls
                self.driver.refresh()
                time.sleep(2)
            else:
                print("[WARN] API did not return an IP. Check your Email in config.py.")

        except Exception as e:
            print(f"[CRITICAL ERROR] Scraper crashed: {e}")

        return found_ips