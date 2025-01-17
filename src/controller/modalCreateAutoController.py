
from src.view.modalCreateAutoView import ModalCreateAutoView


class ModalCreateAutoController:
    
    def __init__(self):
        #----------------------------
        self.modal_create_auto = ModalCreateAutoView()


    def setup_connections(self):
        self.modal_create_auto.tree_widget.itemClicked.connect(self.get_value_tree_widget)
        self.modal_create_auto.button_print_phone.clicked.connect(self.set_file_xml)


    def get_modal_create_auto_widget(self):
       #-----------------------------
       self.modal_create_auto = ModalCreateAutoView()
       self.setup_connections()
       return self.modal_create_auto
    
    def get_value_tree_widget(self,item, column):
        print(item.text(column))

    def set_file_xml(self):
        self.modal_create_auto.set_file_xml()
