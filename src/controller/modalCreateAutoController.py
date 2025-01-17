
from src.view.modalCreateAutoView import ModalCreateAutoView
from src.android.androidDeviceManager import AndroidDeviceManager

class ModalCreateAutoController:
    
    def __init__(self):
        #----------------------------
        self.modal_create_auto = ModalCreateAutoView()


        self.adb:AndroidDeviceManager = None
        self.bounds = None


    def setup_connections(self):
        self.modal_create_auto.tree_widget.itemClicked.connect(self.get_value_tree_widget)
        self.modal_create_auto.button_print_phone.clicked.connect(self.set_file_xml)
        self.modal_create_auto.button_action_phone.clicked.connect(self.action_phone_execute)


    def get_modal_create_auto_widget(self):
       #-----------------------------
       self.modal_create_auto = ModalCreateAutoView()
       self.setup_connections()
       self.adb = AndroidDeviceManager()
       self.adb.connect_device()

       return self.modal_create_auto
  

    def get_value_tree_widget(self,item, column):
       self.bounds = item.text(column)

    def set_file_xml(self):
        self.adb.dump_screen_xml()
        self.modal_create_auto.set_file_xml()

    def action_phone_execute(self):
        self.adb.execute_click_screen(self.bounds)

