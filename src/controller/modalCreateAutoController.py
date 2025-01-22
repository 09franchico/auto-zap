
from src.view.modalCreateAutoView import ModalCreateAutoView
from src.android.androidDeviceManager import AndroidDeviceManager
from PIL import Image, ImageDraw
import re
from PySide6.QtCore import QThread, Signal
import time



class ModalCreateAutoController:
    
    def __init__(self):
        #----------------------------
        self.modal_create_auto_view = ModalCreateAutoView()
        self.adb:AndroidDeviceManager = None
        self.bounds = None
        self.thread_xml = None
        self.add_list_auto =[]


    def setup_connections(self):
        self.modal_create_auto_view.tree_widget.itemClicked.connect(self.get_value_tree_widget)
        self.modal_create_auto_view.button_print_phone.clicked.connect(self.set_file_xml_thread)
        self.modal_create_auto_view.button_action_phone.clicked.connect(self.action_phone_execute)
        self.modal_create_auto_view.button_add_bound.clicked.connect(self.add_bounds_list)
        self.modal_create_auto_view.button_execute_bound.clicked.connect(self.execute_bounds)
        self.modal_create_auto_view.button_back_screen.clicked.connect(self.back_screen)


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
            image.save("imagem_roi.png")
            self.modal_create_auto_view.set_image_screen("imagem_roi.png")
        except Exception as e:
            print(f"Erro ao desenhar o retângulo na imagem: {e}")


    def set_file_xml_thread(self):

        if self.thread_xml and self.thread_xml.isRunning():
            print("Thread anterior ainda está ativa. Aguardando término.")
            return

        self.thread_xml = XmlGenThread(
            self.adb
        )
        self.thread_xml.finished.connect(self.handle_thread_finished)
        self.thread_xml.finished.connect(self.cleanup_thread)
        self.thread_xml.start()

    def add_bounds_list(self):
        if self.bounds is not None:
            self.add_list_auto.append(self.bounds)

    def execute_bounds(self):
        if self.add_list_auto:
           self.adb.execute_auto_screen(self.add_list_auto)

    def back_screen(self):
        if self.adb is not None:
            self.adb.back_screen()

    def cleanup_thread(self,msg):
        self.thread_xml = None

    def handle_thread_finished(self,msg):
        self.modal_create_auto_view.set_image_screen('screenshot.png')
        self.modal_create_auto_view.set_file_xml()

    def action_phone_execute(self):
        self.adb.execute_click_screen(self.bounds)

    def teste(self):
        file_path = "movimentos_touchscreen.txt"
        event_regex = re.compile(r"0035 (\w+)|0036 (\w+)")
        x = None  
        y = None 
        with open(file_path, "r") as file:
            for line in file:
                match = event_regex.search(line)
                if match:
                    if match.group(1): 
                        x = int(match.group(1), 16)
                        print(f"Eixo X: {x}")
                    elif match.group(2):
                        y = int(match.group(2), 16)
                        print(f"Eixo Y: {y}")
                
                    if x is not None and y is not None:
                        print(f"Executando click em: Eixo X: {x}, Eixo Y: {y}")
                        self.adb.click(x, y)
                        time.sleep(1) 
                        x = None
                        y = None






class XmlGenThread(QThread):

    finished = Signal(str)

    def __init__(self,
                 adb,
                 parent=None):
        super().__init__(parent)

        self.adb:AndroidDeviceManager = adb
      
    def run(self):
        try:
            self.adb.dump_screen_xml()
            self.finished.emit(f"DUMP REALIZADO COM SUCESSO")
        
        except Exception as e:
            print(f"Erro ao recortar a imagem: {e}")

