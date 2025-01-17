
from src.view.modalCreateAutoView import ModalCreateAutoView


class ModalCreateAutoController:
    
    def __init__(self):
        #----------------------------
        self.modal_create_auto = ModalCreateAutoView(f'C:/Users/franc/OneDrive/Área de Trabalho/DEV/Python/projeto-pyside/outros/window_dump.xml')

        
    def get_modal_create_auto_widget(self):
       self.modal_create_auto = ModalCreateAutoView(
           f'C:/Users/franc/OneDrive/Área de Trabalho/DEV/Python/projeto-pyside/outros/window_dump.xml'
           )
       return self.modal_create_auto
