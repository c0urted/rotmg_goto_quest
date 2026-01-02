import win32gui
import win32con
import win32com.client
import time
import pyperclip
import pyautogui

class WinApiManager:
    def __init__(self, window_title):
        self.window_title = window_title
        self.hwnd = None
        self.shell = win32com.client.Dispatch("WScript.Shell")

    def find_window(self):
        self.hwnd = win32gui.FindWindow(None, self.window_title)
        return bool(self.hwnd)

    def send_chat_command(self, command):
        """
        The 'Flash Focus' Method:
        1. Remember current window.
        2. Swap to Game -> Paste -> Enter.
        3. Swap back to current window.
        """
        if not self.find_window():
            print("[Error] Game window not found.")
            return False

        print(f"[Action] Sending command: {command}")

        # 1. Save the window you are currently using
        previous_window = win32gui.GetForegroundWindow()
        
        try:
            # 2. Force Game to Foreground
            # The 'Alt' key press helps bypass Windows focus restrictions
            self.shell.SendKeys('%') 
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE) # Un-minimize if needed
            time.sleep(0.05)
            
            # 3. Copy to Clipboard
            pyperclip.copy(command)

            # 4. Open Chat -> Paste -> Submit (Using PyAutoGUI for reliability)
            pyautogui.press('enter')
            time.sleep(0.05)
            
            # We use 'ctrl' + 'v' explicitly
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.05)
            
            pyautogui.press('enter')
            
            # 5. Immediately switch back to what you were doing
            if previous_window and previous_window != self.hwnd:
                win32gui.SetForegroundWindow(previous_window)

            print("[Action] Command sent (Flash Focus complete).")
            return True

        except Exception as e:
            print(f"[Error] Flash Focus failed: {e}")
            # Try to restore focus anyway so user isn't stuck
            if previous_window:
                try: win32gui.SetForegroundWindow(previous_window)
                except: pass
            return False