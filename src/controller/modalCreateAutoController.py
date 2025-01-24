
from src.view.modalCreateAutoView import ModalCreateAutoView
from src.android.androidDeviceManager import AndroidDeviceManager
from PIL import Image, ImageDraw
import re
from PySide6.QtCore import QThread, Signal
import time
import json



class ModalCreateAutoController:
    
    def __init__(self):
        #----------------------------
        self.modal_create_auto_view = ModalCreateAutoView()
        self.adb:AndroidDeviceManager = None
        self.bounds = None
        self.thread_xml = None
        self.thread_auto_click = None
        self.thread_processar_click = None
        self.add_list_auto =[]
        self.auto_clicks = []


    def setup_connections(self):
        self.modal_create_auto_view.table_widget.cellClicked.connect(self.on_cell_clicked)
        self.modal_create_auto_view.button_print_phone.clicked.connect(self.set_file_xml_thread)
        self.modal_create_auto_view.button_action_phone.clicked.connect(self.action_phone_execute)
        self.modal_create_auto_view.button_add_bound.clicked.connect(self.add_bounds_list)
        self.modal_create_auto_view.button_execute_bound.clicked.connect(self.execute_bounds)
        self.modal_create_auto_view.button_back_screen.clicked.connect(self.back_screen)
        self.modal_create_auto_view.button_auto_click_screen_phone.clicked.connect(self.auto_click_screen_phone)
        self.modal_create_auto_view.button_stop_auto_click_screen_phone.clicked.connect(self.stop_auto_click_screen_phone)
        self.modal_create_auto_view.button_salvar_auto.clicked.connect(self.salvar_automatico)
        self.modal_create_auto_view.button_load_file_auto.clicked.connect(self.load_file_auto)


    def get_modal_create_auto_widget(self):
       self.modal_create_auto_view = ModalCreateAutoView()
       self.setup_connections()
       self.adb = AndroidDeviceManager()
       self.adb.connect_device()
       return self.modal_create_auto_view
  
    def on_cell_clicked(self, row, column):
        if row is None or column is None:
            return
        
        item = self.modal_create_auto_view.table_widget.item(row, column)
        if item is None:
            return
        self.bounds = item.text()
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
        self.thread_xml.start()

    def auto_click_screen_phone(self):

        if self.thread_auto_click and self.thread_auto_click.isRunning():
            print("Thread anterior ainda está ativa. Aguardando término.")
            return
        
        self.modal_create_auto_view.add_text_image_label("[ REALIZANDO A AUTOMACAO DOS CLICKS - ON ]")
        self.thread_auto_click = AutoScreenThread(
            self.adb
        )
        self.thread_auto_click.finished.connect(self.cleanup_thread_auto)
        self.thread_auto_click.start()


    def coordenation_screen_text(self):

        file_path = "movimentos_touchscreen.txt"
        event_regex = re.compile(r"0035 (\w+)|0036 (\w+)")
        x = None  
        y = None 
        clicks = []
        with open(file_path, "r") as file:
            for line in file:
                match = event_regex.search(line)
                if match:
                    if match.group(1): 
                        x = int(match.group(1), 16)
                    elif match.group(2):
                        y = int(match.group(2), 16)

                    if x is not None and y is not None:
                        print(f"Adicionado ao array: {(x, y)}")
                        clicks.append((x, y))
                        x = None
                        y = None

        self.clear_file()

        return clicks
    

    def clear_file(self):
        file_path = "movimentos_touchscreen.txt"
        try:
            with open(file_path, "w") as file:
                file.truncate(0)
            print(f"Arquivo {file_path} limpo com sucesso.")
        except Exception as e:
            print(f"Erro ao limpar o arquivo: {e}")


    def execute_click_auto(self):

        if self.thread_processar_click and self.thread_processar_click.isRunning():
            print("Thread anterior ainda está ativa. Aguardando término.")
            return
        
        #-----------------------------
        self.thread_processar_click = AutoScreenExecuteClickThread(
            adb=self.adb,
            clicks=self.auto_clicks
        )
        self.thread_processar_click.finished.connect(self.cleanup_thread_processar_click)
        self.thread_processar_click.start()
        self.modal_create_auto_view.add_text_image_label("[ PROCESSANDO CLICKS ]")


    def salvar_automatico(self):
        if self.auto_clicks:
           self.modal_create_auto_view.save_json_click_xy(self.auto_clicks)

    def load_file_auto(self):
        file_path = self.modal_create_auto_view.open_auto_file()
        if file_path: 
            try:
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    data:dict = json.load(file)
                    self.auto_clicks = data.get('clicks_xy')
                    print(data.get('clicks_xy'))

            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar o arquivo JSON: {e}")
            except Exception as e:
                print(f"Ocorreu um erro ao carregar o arquivo JSON: {e}")
        else:
            print("Nenhum arquivo foi selecionado.")



    def stop_auto_click_screen_phone(self):
        if self.adb:
            self.adb.stop_capture()
            self.auto_clicks = self.coordenation_screen_text()
            self.modal_create_auto_view.add_text_image_label("[ AUTOMACAO PARADA COM SUCESSO - OFF ]")
            

    def add_bounds_list(self):
        if self.bounds is not None:
            self.add_list_auto.append(self.bounds)

    def execute_bounds(self):
        self.execute_click_auto()

    def back_screen(self):
        if self.adb is not None:
            self.adb.back_screen()

    def cleanup_thread(self,msg):
        self.thread_xml = None

    def cleanup_thread_auto(self,msg):
        self.thread_auto_click = None

    def handle_thread_finished(self,msg):
        self.modal_create_auto_view.set_image_screen('screenshot.png')
        self.modal_create_auto_view.set_file_xml()
        self.thread_xml = None

    def action_phone_execute(self):
        if self.bounds is not None:
           self.adb.execute_click_screen(self.bounds)

    def cleanup_thread_processar_click(self,msg):
        self.modal_create_auto_view.add_text_image_label("[ AUTOMACAO DE CLICKS FINALIZADO ]")
        self.thread_processar_click = None

    

class AutoScreenExecuteClickThread(QThread):

    finished = Signal(str)

    def __init__(self,
                 adb,
                 clicks,
                 parent=None):
        super().__init__(parent)

        self.adb:AndroidDeviceManager = adb
        self.clicks = clicks
      
    def run(self):
        try:
            self.adb.clear_app_open(1)
            for x, y in self.clicks:
                print(f"Executando click em: Eixo X: {x}, Eixo Y: {y}")
                self.adb.click(x, y)
                time.sleep(1) 
            
            self.finished.emit(f"FINALIZADO CLICKS")
        
        except Exception as e:
            print(f"Erro ao executar AutoScreenThread: {e}")
      



class AutoScreenThread(QThread):

    finished = Signal(str)

    def __init__(self,
                 adb,
                 parent=None):
        super().__init__(parent)

        self.adb:AndroidDeviceManager = adb
      
    def run(self):
        try:
            self.adb.register_toque_screen()
            self.finished.emit(f"EM PROCESSO AUTO-SCREEN")
        
        except Exception as e:
            print(f"Erro ao executar AutoScreenThread: {e}")



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

