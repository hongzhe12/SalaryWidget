import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Key, KeyCode, Listener

from hotkey_manager import HotkeyManager


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("未触发热键", self)
        self.label.setGeometry(50, 50, 200, 30)

        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.on_hotkey_pressed)
        self.hotkey_manager.esc_pressed.connect(self.on_esc_pressed)
        self.hotkey_manager.start_listen()

    def on_hotkey_pressed(self):
        self.label.setText("热键已触发")

    def on_esc_pressed(self):
        self.label.setText("退出！")

    def closeEvent(self, event):
        self.hotkey_manager.stop_listen()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("全局键盘监听示例")
    window.setGeometry(100, 100, 300, 200)
    window.show()
    sys.exit(app.exec())
