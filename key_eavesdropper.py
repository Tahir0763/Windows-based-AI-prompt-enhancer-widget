from pynput import keyboard
import time

import threading

class KeyEavesdropper:
    def __init__(self, callback):
        self.callback = callback
        self.controller = keyboard.Controller()
        self.listener = None

    def on_activate(self):
        threading.Thread(target=self._perform_copy, daemon=True).start()

    def _perform_copy(self):
        # 1. Release modifier keys that might be held down by the user (fixing Ctrl+Alt+C issue)
        self.controller.release(keyboard.Key.alt)
        self.controller.release(keyboard.Key.alt_l)
        self.controller.release(keyboard.Key.alt_r)
        self.controller.release(keyboard.Key.ctrl) # Release user's ctrl to be clean
        time.sleep(0.1)

        # 2. Select All (Ctrl+A) - Re-added per user request
        self.controller.press(keyboard.Key.ctrl)
        time.sleep(0.05)
        self.controller.press('a')
        time.sleep(0.05)
        self.controller.release('a')
        self.controller.release(keyboard.Key.ctrl)
        time.sleep(0.1)

        # 3. Copy (Ctrl+C) - Explicit press/release
        self.controller.press(keyboard.Key.ctrl)
        time.sleep(0.05)
        self.controller.press('c')
        time.sleep(0.05)
        self.controller.release('c')
        self.controller.release(keyboard.Key.ctrl)
        
        # Increased delay to ensure clipboard is populated
        time.sleep(0.8)
        
        # 3. Notify callback to read clipboard
        if self.callback:
            self.callback()

    def start(self):
        # Listen for Ctrl+Alt+E
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+e': self.on_activate
        })
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
