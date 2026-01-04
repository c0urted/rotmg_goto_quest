import cv2
import numpy as np
import pyautogui
import win32gui
import imutils # Make sure to pip install imutils
import config
import os

class StateDetector:
    def __init__(self, win_manager):
        # We store win_manager so we can find the window coordinates later
        self.win_manager = win_manager
        self.templates = []
        
        # Load ALL images defined in config
        # If config doesn't have SAFE_IMAGES, default to looking for 'nexus_portal.png'
        image_list = getattr(config, "SAFE_IMAGES", ["nexus_portal.png"])
        
        for img_name in image_list:
            if os.path.exists(img_name):
                # Load in Grayscale (0)
                templ = cv2.imread(img_name, 0)
                if templ is not None:
                    self.templates.append(templ)
                    print(f"[System] Loaded detection template: {img_name}")
        
        if not self.templates:
            print("[Warning] No detection images found! Bot is running in BLIND MODE (Safety checks disabled).")

    def get_game_screenshot(self):
        """Captures ONLY the game window content."""
        hwnd = self.win_manager.hwnd
        if not hwnd:
            self.win_manager.find_window()
            hwnd = self.win_manager.hwnd
            if not hwnd: return None

        try:
            rect = win32gui.GetWindowRect(hwnd)
            x, y, right, bottom = rect
            w = right - x
            h = bottom - y
            
            # Simple validation to ensure window isn't minimized (0x0 size)
            if w <= 0 or h <= 0: return None
            
            return pyautogui.screenshot(region=(x, y, w, h))
        except:
            return None

    def is_in_safe_zone(self):
        """
        Checks if we are in a 'Safe' area (Nexus/Ghall).
        """
        if not self.templates:
            return True # Blind mode = Always safe

        screenshot = self.get_game_screenshot()
        if screenshot is None:
            return False

        gray_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        # Use config settings if they exist, otherwise defaults
        scale_min = getattr(config, "SCALE_MIN", 0.5)
        scale_max = getattr(config, "SCALE_MAX", 1.5)
        scale_steps = getattr(config, "SCALE_STEPS", 10)

        for template in self.templates:
            template_h, template_w = template.shape[:2]
            
            # Multi-Scale Search
            for scale in np.linspace(scale_min, scale_max, scale_steps)[::-1]:
                new_w = int(template_w * scale)
                new_h = int(template_h * scale)
                
                if new_w > gray_screen.shape[1] or new_h > gray_screen.shape[0]:
                    continue

                resized_template = imutils.resize(template, width=new_w)
                result = cv2.matchTemplate(gray_screen, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)

                if max_val >= 0.8:
                    return True

        return False

    # Alias for compatibility with older code calling is_in_nexus()
    def is_in_nexus(self):
        return self.is_in_safe_zone()