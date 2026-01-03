import cv2
import numpy as np
import pyautogui
import os
import win32api

class StateDetector:
    def __init__(self):
        # Calculate screen center once to save math later
        self.screen_w = win32api.GetSystemMetrics(0)
        self.screen_h = win32api.GetSystemMetrics(1)
        
        # Define a 600x600 box in the middle of the screen
        self.roi_left = (self.screen_w // 2) - 300
        self.roi_top = (self.screen_h // 2) - 300
        self.roi_width = 600
        self.roi_height = 600
        
        # Pre-load the template in Grayscale
        if os.path.exists("nexus_portal.png"):
            self.template = cv2.imread("nexus_portal.png", 0) # 0 = Grayscale mode
        else:
            self.template = None

    def is_in_nexus(self):
        if self.template is None:
            return True # Blind mode

        try:
            # 1. Screenshot ONLY the Region of Interest (Center of screen)
            screenshot = pyautogui.screenshot(region=(self.roi_left, self.roi_top, self.roi_width, self.roi_height))
            
            # 2. Convert to Grayscale (Faster)
            gray_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            
            # 3. Match
            result = cv2.matchTemplate(gray_screen, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            return max_val >= 0.8
            
        except Exception:
            return True