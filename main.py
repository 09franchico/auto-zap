from PySide6.QtWidgets import (
    QApplication
)
from qt_material import apply_stylesheet
import sys
from src.controller.mainController import MainController

class App:
    
    def __init__(self,app:QApplication):
        self.app = app
        super().__init__()

        #------------------------- theme
        # apply_stylesheet(app=self.app, theme="light_blue.xml",css_file='custom.css')
        # qdarktheme.setup_theme("light")
        self.main_controller = MainController()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = App(app=app)
    sys.exit(app.exec())
