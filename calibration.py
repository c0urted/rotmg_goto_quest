import pyautogui
import time
import json
import win32gui
import keyboard
import ctypes
import os

# DPI Fix so it clicks the right spot
try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
except: ctypes.windll.user32.SetProcessDPIAware()

def get_window_rect(title):
    try:
        hwnd = win32gui.FindWindow(None, title)
        return win32gui.GetWindowRect(hwnd) if hwnd else None
    except: return None

# --- MAIN ---
print("--- V1 SAFETY CALIBRATOR ---")
print("1. Stand in Nexus.")
print("2. Hover over a static UI element (Shop/Fame Icon).")
print("3. Press 'Ctrl+B' to ADD pixel.")
print("4. Add 3-5 spots.")
print("5. Press 'Ctrl+S' to SAVE.")

saved_pixels = []

while True:
    # Add Pixel
    if keyboard.is_pressed('ctrl+b'):
        if 'rel_x' in locals():
            saved_pixels.append({"rel_x": rel_x, "rel_y": rel_y, "color": (r, g, b)})
            print(f"\n[+] Pixel Saved: {len(saved_pixels)}")
            time.sleep(0.5)

    # Save & Quit
    if keyboard.is_pressed('ctrl+s'):
        with open("pixel_config.json", "w") as f:
            json.dump(saved_pixels, f)
        print("Saved 'pixel_config.json'. You can close this.")
        break

    # Tracker
    rect = get_window_rect("RotMGExalt")
    if rect:
        win_x, win_y, _, _ = rect
        mouse_x, mouse_y = pyautogui.position()
        rel_x, rel_y = mouse_x - win_x, mouse_y - win_y
        try:
            r, g, b = pyautogui.pixel(mouse_x, mouse_y)
            print(f"\rPixels: {len(saved_pixels)} | RGB:({r},{g},{b})   ", end="")
        except: pass
    time.sleep(0.05)