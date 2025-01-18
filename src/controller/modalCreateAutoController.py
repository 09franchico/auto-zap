
from src.view.modalCreateAutoView import ModalCreateAutoView
from src.android.androidDeviceManager import AndroidDeviceManager
from PIL import Image, ImageDraw
import re
from PySide6.QtCore import QThread, Signal



class ModalCreateAutoController:
    
    def __init__(self):
        #----------------------------
        self.modal_create_auto_view = ModalCreateAutoView()
        self.adb:AndroidDeviceManager = None
        self.bounds = None


    def setup_connections(self):
        self.modal_create_auto_view.tree_widget.itemClicked.connect(self.get_value_tree_widget)
        self.modal_create_auto_view.button_print_phone.clicked.connect(self.set_file_xml_thread)
        self.modal_create_auto_view.button_action_phone.clicked.connect(self.action_phone_execute)


    def get_modal_create_auto_widget(self):
       self.modal_create_auto_view = ModalCreateAutoView()
       self.setup_connections()
       self.adb = AndroidDeviceManager()
       self.adb.connect_device()
       return self.modal_create_auto_view
  

    def get_value_tree_widget(self, item, column):
        self.bounds = item.text(column)
        match = re.search(r'\[(\d+),(\d+)]\[(\d+),(\d+)]', self.bounds)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            self.draw_rectangle_on_image("screenshot.png", x1, y1, x2, y2)

    def draw_rectangle_on_image(self, image_path, x1, y1, x2, y2):
        try:

            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            rectangle_color = (255, 0, 0)
            rectangle_width = 3 
            draw.rectangle([x1, y1, x2, y2], outline=rectangle_color, width=rectangle_width)
            image.save("cropped_image.png")
            self.modal_create_auto_view.set_image_screen(image)
        except Exception as e:
            print(f"Erro ao desenhar o retângulo na imagem: {e}")

    # def crop_image(self, image_path, x1, y1, x2, y2):
    #     try:
    #         image = Image.open(image_path)
    #         cropped_image = image.crop((x1, y1, x2, y2))
    #         cropped_image.save("cropped_image.png")
    #         self.modal_create_auto_view.set_image_screen(image)
    #     except Exception as e:
    #         print(f"Erro ao recortar a imagem: {e}")


    def set_file_xml_thread(self):
        # self.thread_xml = None
        # self.thread_xml = XmlGenThread(
        #         self.adb,
        #         self.modal_create_auto_view
        #     )
        # self.thread_xml.finished.connect(self.handle_thread_finished)
        # self.thread_xml.start()

        self.adb.dump_screen_xml()
        self.modal_create_auto_view.set_file_xml()

    def handle_thread_finished(self,msg):
        print("-------------------", msg)

    def action_phone_execute(self):
        self.adb.execute_click_screen(self.bounds)






class XmlGenThread(QThread):

    finished = Signal(str)

    def __init__(self,
                 adb,
                 controller, 
                 parent=None):
        super().__init__(parent)

        self.adb:AndroidDeviceManager = adb
        self.modal_create_view:ModalCreateAutoView = controller
      
    def run(self):
        try:
            self.adb.dump_screen_xml()
            self.modal_create_view.set_file_xml()
            self.finished.emit(f"SUCESSO NA GERACAO DE IMAGEM")
        
        except Exception as e:
            print(f"Erro ao recortar a imagem: {e}")

