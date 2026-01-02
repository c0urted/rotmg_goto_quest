import cv2
import numpy as np
import os

class StateDetector:
    def __init__(self, api_manager):
        self.api = api_manager
        # Load the reference image of the Nexus floor
        if os.path.exists("nexus_pattern.png"):
            self.template = cv2.imread("nexus_pattern.png", cv2.IMREAD_UNCHANGED)
            # Remove alpha channel if present (OpenCV matchTemplate prefers 3 channels)
            if self.template.shape[2] == 4:
                self.template = self.template[:, :, :3]
        else:
            print("[Error] nexus_pattern.png not found! Nexus detection will fail.")
            self.template = None

    def is_in_nexus(self):
        """
        Scans the screen for the Nexus floor texture.
        Returns True if the texture is found with high confidence.
        """
        if self.template is None: return False

        # 1. Capture Screen
        screen = self.api.capture_background()
        if screen is None: return False

        # 2. Convert to standard BGR (remove alpha from screenshot)
        screen_bgr = screen[:, :, :3]

        # 3. Template Matching (The heavy lifting)
        # This slides the 'nexus_pattern' over the 'screen' looking for a match
        result = cv2.matchTemplate(screen_bgr, self.template, cv2.TM_CCOEFF_NORMED)
        
        # 4. Check confidence
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # Threshold: 0.8 means "80% match". Adjust this if it fails.
        return max_val > 0.8