import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import threading

# Import our modules
from overlay import DraggableWidget
from key_eavesdropper import KeyEavesdropper
from ai_handler import AIHandler

class Bridge(QObject):
    """
    Bridge between non-GUI thread (pynput) and GUI thread (PyQt)
    """
    text_ready = pyqtSignal(str)
    trigger_clipboard = pyqtSignal()

def main():
    app = QApplication(sys.argv)
    
    # 1. Setup UI
    widget = DraggableWidget()
    widget.show()
    
    # 2. Setup AI
    ai = AIHandler() # Will look for os.getenv("OPENAI_API_KEY")
    
    # 3. Setup Bridge
    bridge = Bridge()
    
    def run_ai_processing(text):
        # Background worker for AI
        enhanced = ai.enhance_text(text)
        if enhanced:
            bridge.text_ready.emit(enhanced)
    
    def on_clipboard_trigger():
        # This is emitted from pynput thread
        bridge.trigger_clipboard.emit()

    def handle_clipboard_read():
        # Runs in Main Thread (safe for clipboard)
        clipboard = app.clipboard()
        text = clipboard.text()
        print(f"DEBUG: Read from clipboard: {repr(text)}")
        
        # Spawn thread for AI to avoid freezing UI
        if text and len(text.strip()) > 0:
            threading.Thread(target=run_ai_processing, args=(text,), daemon=True).start()
        else:
            print("Clipboard empty or invalid.")

    # Connect signals
    bridge.text_ready.connect(widget.update_text)
    bridge.trigger_clipboard.connect(handle_clipboard_read)
    
    # 4. Setup Key Listener
    # Provide callback that notifies bridge
    listener = KeyEavesdropper(callback=on_clipboard_trigger)
    listener.start()
    
    print("Application Started. Press Ctrl+Alt+E to enhance selected text.")
    
    # Run loop
    try:
        sys.exit(app.exec())
    finally:
        listener.stop()

if __name__ == "__main__":
    main()
