import sys
import os
import webbrowser
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QHBoxLayout
)
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, Qt
from datetime import datetime
from pynput import keyboard
import mss


class KeyListenerThread(QThread):
    screenshot_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_keys = set()
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        # Add the pressed key to the set
        self.current_keys.add(key)
        # Check if Ctrl and Space are pressed
        if (
            keyboard.Key.space in self.current_keys and
            (keyboard.Key.ctrl_l in self.current_keys or keyboard.Key.ctrl_r in self.current_keys)
        ):
            self.screenshot_signal.emit()

    def on_release(self, key):
        # Remove the released key from the set
        self.current_keys.discard(key)

    def run(self):
        self.listener.start()
        self.listener.join()

    def stop(self):
        self.listener.stop()
        self.quit()


class ScreenshotApp(QWidget):
    screenshot_taken = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.base_screenshot_folder = "screenshots"
        self.session_folder = None

        self.key_listener = KeyListenerThread()
        self.key_listener.screenshot_signal.connect(self.capture_screenshot)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('ScreenshotBundle')

        # Set the window icon
        self.setWindowIcon(QIcon('icon.ico'))

        # Set a minimum size for the window
        self.setMinimumSize(550, 200)

        # Apply dark mode
        self.apply_dark_mode()

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Start/Stop button
        self.start_stop_button = QPushButton('Start', self)
        self.start_stop_button.setFixedHeight(60)
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        self.start_stop_button.clicked.connect(self.toggle_screenshots)
        self.layout.addWidget(self.start_stop_button)

        # Instruction label
        self.instruction_label = QLabel(
            'Press Ctrl + Space to take a screenshot', self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.instruction_label)

        # Horizontal layout for checkbox and folder button
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(15)

        # Capture All Screens checkbox
        self.capture_all_checkbox = QCheckBox("Capture All Screens", self)
        self.capture_all_checkbox.setStyleSheet("font-size: 18px;")
        self.h_layout.addWidget(self.capture_all_checkbox)

        # Open Screenshots Folder button
        self.open_folder_button = QPushButton('Open Screenshots Folder', self)
        self.open_folder_button.setFixedHeight(50)
        self.open_folder_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.open_folder_button.clicked.connect(self.open_screenshots_folder)
        self.h_layout.addWidget(self.open_folder_button)

        self.layout.addLayout(self.h_layout)

        self.setLayout(self.layout)

    def apply_dark_mode(self):
        # Define the dark stylesheet
        dark_stylesheet = """
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        QCheckBox {
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
        }
        """
        # Apply the stylesheet to the application
        self.setStyleSheet(dark_stylesheet)

    def toggle_screenshots(self):
        if not self.is_running:
            self.start_screenshots()
        else:
            self.stop_screenshots()

    def start_screenshots(self):
        self.is_running = True
        self.start_stop_button.setText('Stop')
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                background-color: #f44336;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        # Create a new session folder with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_folder = os.path.join(
            self.base_screenshot_folder, f"session_{timestamp}")
        os.makedirs(self.session_folder, exist_ok=True)

        self.key_listener.start()

    def stop_screenshots(self):
        self.is_running = False
        self.start_stop_button.setText('Start')
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        self.key_listener.stop()

        # Restart the key listener for future use
        self.key_listener = KeyListenerThread()
        self.key_listener.screenshot_signal.connect(self.capture_screenshot)

    def open_screenshots_folder(self):
        if self.session_folder and os.path.exists(self.session_folder):
            threading.Thread(target=lambda: webbrowser.open(
                f'file://{os.path.abspath(self.session_folder)}')).start()
        else:
            if not os.path.exists(self.base_screenshot_folder):
                os.makedirs(self.base_screenshot_folder)
            threading.Thread(target=lambda: webbrowser.open(
                f'file://{os.path.abspath(self.base_screenshot_folder)}')).start()

    @pyqtSlot()
    def capture_screenshot(self):
        if self.is_running:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            if self.capture_all_checkbox.isChecked():
                # Capture all screens using mss
                with mss.mss() as sct:
                    for idx, monitor in enumerate(sct.monitors[1:], start=1):
                        img = sct.grab(monitor)
                        screenshot_filename = f'screenshot_{
                            timestamp}_screen{idx}.png'
                        screenshot_path = os.path.join(
                            self.session_folder, screenshot_filename)
                        mss.tools.to_png(img.rgb, img.size,
                                         output=screenshot_path)
            else:
                # Capture the screen the mouse is on
                cursor_pos = QCursor.pos()
                screen = QApplication.screenAt(cursor_pos)
                if screen:
                    monitor = screen.geometry()
                    with mss.mss() as sct:
                        monitor_dict = {
                            "left": monitor.x(),
                            "top": monitor.y(),
                            "width": monitor.width(),
                            "height": monitor.height()
                        }
                        img = sct.grab(monitor_dict)
                        screenshot_filename = f'screenshot_{timestamp}.png'
                        screenshot_path = os.path.join(
                            self.session_folder, screenshot_filename)
                        mss.tools.to_png(img.rgb, img.size,
                                         output=screenshot_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    ex.show()
    sys.exit(app.exec_())
