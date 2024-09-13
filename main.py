import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import time


class MainWindow(QMainWindow):
    def __init__(self, process):
        super().__init__()
        self.__starting_time = time.time()
        self.setWindowTitle("Bash Script Controller")
        self.setGeometry(100, 100, 300, 100)
        self.process = process

        self.stop_button = QPushButton("Stop Script", self)
        self.stop_button.setGeometry(50, 30, 200, 40)
        self.stop_button.clicked.connect(self.stop_script)

    def stop_script(self):
        self.process.terminate()
        # read_and_download_data()
        self.process.wait()
        self.close()


def run_bash_script():
    command = "wsl ./sdk_src/simple_grabber --channel --serial /dev/ttyUSB0 115200 | py ./ui/menu.py\n"
    process = subprocess.Popen(command, shell=True)
    return process


def reset_data():
    # Cleans the old outputs from last run
    if os.path.exists("locations"):
        for file in os.listdir("locations"):
            os.remove(os.path.join("locations", file))
    else:
        os.makedirs("locations")


if __name__ == "__main__":
    reset_data()

    app = QApplication(sys.argv)
    process = run_bash_script()
    window = MainWindow(process)
    window.show()

    sys.exit(app.exec())
