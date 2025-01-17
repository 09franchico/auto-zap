
from src.view.modalCreateAutoView import ModalCreateAutoView
from src.android.androidDeviceManager import AndroidDeviceManager
from PIL import Image
import re

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
  

    def get_value_tree_widget(self, item, column):
        self.bounds = item.text(column)

        match = re.search(r'\[(\d+),(\d+)]\[(\d+),(\d+)]', self.bounds)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            print(f"Coordenadas: ({x1}, {y1}), ({x2}, {y2})")
            self.crop_image("screenshot.png", x1, y1, x2, y2)

    def crop_image(self, image_path, x1, y1, x2, y2):
        try:
            
            image = Image.open(image_path)
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_image.save("cropped_image.png")
            self.modal_create_auto.set_image_screen(cropped_image)
            # print("Imagem recortada salva como 'cropped_image.png'.")
        except Exception as e:
            print(f"Erro ao recortar a imagem: {e}")

    def set_file_xml(self):
        self.adb.dump_screen_xml()
        self.modal_create_auto.set_file_xml()

    def action_phone_execute(self):
        self.adb.execute_click_screen(self.bounds)

