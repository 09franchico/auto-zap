from PySide6.QtWidgets import (
    QApplication
)
import sys
from src.controller.mainController import MainController
from src.android.adb_server import StartDaemon
from src.controller.modalCreateAutoController import ModalCreateAutoController

class App:
    
    def __init__(self,app:QApplication):
        self.app = app
        super().__init__()

        #---------------------
        StartDaemon().start()
        self.main_controller = MainController()
        self.modal_create_auto_controller = ModalCreateAutoController()
        
        self.main_controller.set_controller(self.modal_create_auto_controller)

     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = App(app=app)
    sys.exit(app.exec())
