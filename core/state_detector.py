import pyautogui
import json
import os
import win32gui
import ctypes

try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except: ctypes.windll.user32.SetProcessDPIAware()

class StateDetector:
    def __init__(self, win_manager):
        self.pixel_list = self.load_config()

    def load_config(self):
        if os.path.exists("pixel_config.json"):
            try:
                with open("pixel_config.json", "r") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else [data]
            except: pass
        return []

    def is_in_nexus(self):
        if not self.pixel_list: return True
        hwnd = win32gui.FindWindow(None, "RotMGExalt")
        if not hwnd: return False
        try:
            rect = win32gui.GetWindowRect(hwnd)
            win_x, win_y = rect[0], rect[1]
            matches = 0
            for p in self.pixel_list:
                if pyautogui.pixelMatchesColor(win_x + p["rel_x"], win_y + p["rel_y"], tuple(p["color"]), tolerance=10):
                    matches += 1
            threshold = len(self.pixel_list) - 1 if len(self.pixel_list) > 1 else 1
            return matches >= threshold
        except: return False