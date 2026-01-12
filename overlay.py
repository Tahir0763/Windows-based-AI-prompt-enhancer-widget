from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QApplication, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QColor, QPalette, QFont, QCursor

class DraggableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.dragPos = QPoint()
        self.current_text = ""
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Dimensions
        self.resize(450, 200)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10) # Margin for shadow
        
        # Content Frame (The actual visible pod)
        self.frame = QWidget()
        self.frame.setStyleSheet("""
            QWidget#MainFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e2f, stop:1 #2d2d44);
                color: #E0E0E0;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        self.frame.setObjectName("MainFrame")
        
        # Drop Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.frame.setGraphicsEffect(shadow)

        # Frame Layout
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(5)
        
        # --- HEADER ---
        header = QWidget()
        header.setStyleSheet("background: rgba(255, 255, 255, 0.05); border-top-left-radius: 16px; border-top-right-radius: 16px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 8, 10, 8)
        
        # Title
        title = QLabel("AI Enhanced")
        title.setStyleSheet("font-weight: bold; font-size: 13px; color: #a0a0ff;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgba(255, 255, 255, 0.6);
                border: none;
                font-size: 20px;
                font-weight: bold;
                padding-bottom: 2px;
            }
            QPushButton:hover {
                color: #ff5555;
            }
        """)
        self.close_btn.clicked.connect(QApplication.quit)
        header_layout.addWidget(self.close_btn)
        
        frame_layout.addWidget(header)
        
        # --- BODY ---
        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(20, 10, 20, 10)
        
        self.container = QLabel("Waiting for input...")
        self.container.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.container.setWordWrap(True)
        self.container.setStyleSheet("""
            font-size: 14px; 
            line-height: 1.4; 
            background: transparent;
            color: #d0d0d0;
        """)
        body_layout.addWidget(self.container)
        body_layout.addStretch()
        
        frame_layout.addLayout(body_layout)
        
        # --- FOOTER ---
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(20, 0, 20, 15)
        footer_layout.addStretch()
        
        self.copy_btn = QPushButton("Copy Text")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.setFixedSize(100, 32)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #5b5b8c;
                color: white;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #6c6c9d;
            }
            QPushButton:pressed {
                background-color: #4a4a70;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        footer_layout.addWidget(self.copy_btn)
        
        frame_layout.addLayout(footer_layout)
        
        self.frame.setLayout(frame_layout)
        main_layout.addWidget(self.frame)
        self.setLayout(main_layout)
        
        # Initial Position
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 470, screen.height() - 350)

    def update_text(self, text):
        self.current_text = text
        self.container.setText(text)
        self.container.adjustSize()
        # Adjust window height if text is long (simple logic, can be improved)
        needed_height = self.container.sizeHint().height() + 100
        self.resize(self.width(), max(200, min(needed_height, 600)))

    def copy_to_clipboard(self):
        if self.current_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_text)
            
            # Feedback
            original_text = self.copy_btn.text()
            self.copy_btn.setText("Copied!")
            self.copy_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 12px;
                    border: none;
                }
            """)
            QTimer.singleShot(1500, lambda: self._reset_copy_btn(original_text))

    def _reset_copy_btn(self, text):
        self.copy_btn.setText("Copy Text")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #5b5b8c;
                color: white;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #6c6c9d;
            }
            QPushButton:pressed {
                background-color: #4a4a70;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Allow dragging by clicking anywhere on the frame that isn't a button
            self.dragPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPos)
            event.accept()
