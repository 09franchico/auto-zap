from PySide6.QtWidgets import (
    QApplication
)
import sys
from src.controller.mainController import MainController

class App:
    
    def __init__(self,app:QApplication):
        self.app = app
        super().__init__()

        self.main_controller = MainController()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = App(app=app)
    sys.exit(app.exec())
