from PySide6.QtWidgets import (
    QApplication
)
import sys
from src.controller.mainController import MainController
from src.android.adb_server import StartDaemon

class App:
    
    def __init__(self,app:QApplication):
        self.app = app
        super().__init__()

        #---------------------
        StartDaemon().start()
        self.main_controller = MainController()

     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = App(app=app)
    sys.exit(app.exec())
