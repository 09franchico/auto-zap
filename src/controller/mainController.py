from  src.model.mainModel import MainModel
from src.view.mainView import MainView
from styles import SetupTheme
from openpyxl import Workbook
from openpyxl import load_workbook
from src.android.androidDeviceManager import AndroidDeviceManager
from PySide6.QtCore import QThread, Signal



class AdbThread(QThread):

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, adb_manager:AndroidDeviceManager, phones_number:list, message:list, parent=None):
        super().__init__(parent)
        self.adb_manager = adb_manager
        self.phones_number:list = phones_number
        self.messages:list = message
        self.stop = False

    def run(self):
        try:
            #--------------------------------
            self.stop = False
            self.adb_manager.connect_device()
            self.adb_manager.habiliar_adbkeyboard()

            for phone,msg in zip(self.phones_number, self.messages):

                if self.stop:
                    break

                if phone !="" and msg !="":
                    status, mensagem = self.adb_manager.mensagem_whats(phone, msg)
                    if status:
                        self.finished.emit(f"[{phone}] : {msg}")
                    else:
                        self.error.emit(mensagem)
                        break
                else:
                    self.error.emit("Telefone VAZIO ou INVALIDO")
                
        except Exception as e:
            self.error.emit(str(e))

    def stop_script(self):
        self.stop = True




class MainController:
    
    def __init__(self):
        #----------------------------
        # Instanciar o Model e a View
        self.main_model = MainModel()
        self.main_view = MainView()
        self.theme = SetupTheme()
        self.theme.setupTheme('dark')
        self.theme_select()
        self.value_send_phone = None
        self.data_plan = None
        self.adb = None

        #-------------------------
        self.setup_connections()
        self.main_view.show()


    def theme_select(self):
        self.main_view.combo_box.addItems(self.theme.getTheme())

    def text_selection_phone(self,txt):
        self.value_send_phone = txt

    def setup_connections(self):
        self.main_view.start_process.clicked.connect(self.start_process)
        self.main_view.stop_process.clicked.connect(self.stop_process)
        self.main_view.open_action.triggered.connect(self.open_action_file)
        self.main_view.combo_box.currentTextChanged.connect(self.theme.setupTheme)
        self.main_view.combo_box_colun_envio_phone.currentTextChanged.connect(self.text_selection_phone)

    def open_action_file(self):
        file_path_xlsx = self.main_view.open_action_file()

        if file_path_xlsx is not None:
            self.data_plan = self.get_planilha(file_path_xlsx)
            self.main_view.add_value_combo_box_envio_phone(self.data_plan.get('header_label'))
            self.main_view.show_table_widget_view(data=self.data_plan)

        
    def start_process(self):
        
        telefones = self.main_view.get_column_data(self.value_send_phone)
        
        msg = self.main_view.get_column_data("MENSAGEM")

        if telefones and msg:
            self.adb = AndroidDeviceManager()
            self.adb_thread = AdbThread(self.adb, telefones, msg)
            self.adb_thread.finished.connect(self.on_adb_finished)
            self.adb_thread.error.connect(self.on_adb_error)
            self.adb_thread.start()

        
        # selected_items = self.main_view.table_widget.selectedIndexes()

        # if selected_items:
        #     index = selected_items[0]
        #     item = self.main_view.table_widget.item(index.row(), index.column())

        #     if item:
        #         self.log(f"Item selecionado :: {item.text()}")
        #         telefones = self.main_view.get_column_data("TELEFONE")
        #         msg = self.main_view.get_column_data("MENSAGEM")

        #         self.adb = AndroidDeviceManager()
        #         self.adb_thread = AdbThread(self.adb, telefones, msg)
        #         self.adb_thread.finished.connect(self.on_adb_finished)
        #         self.adb_thread.error.connect(self.on_adb_error)
        #         self.adb_thread.start()

        #     else:
        #         self.log("Nenhum item selecionado ou item vazio.")

        # else:
        #     self.log("Nenhum item selecionado.")



    def on_adb_finished(self,msg):
       self.log(msg=msg)

    def on_adb_error(self, error_message):
       self.log(f"Erro : {error_message}")
     


    def stop_process(self):
        if self.adb is not None:
           self.adb_thread.stop_script()
           self.adb.reset_adbkeyboard()

        
    def get_planilha(self,path):
        try:
            workbook = load_workbook(path)
            sheet = workbook.active
            
            header_label = []
            data = []

            for i, row in enumerate(sheet.iter_rows(values_only=True)):
                if i == 0: 
                    header_label = [cell if cell is not None else '' for cell in row]
                else: 
                    data.append([cell if cell is not None else '' for cell in row])
            
            result = {
                "header_label": header_label,
                "data": data
            }
            
            return result
        
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            return None
        

    def create_planilha(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Minha Planilha"

        ws.append(["NOME", "EMAIL", "TELEFONE","MENSAGEM"])
        ws.append([f"Francisco santos", "fra@gmail.com", "92993160919","OLA AQUI È UM TESTE DE MENSAGEM QUE SERÀ ENVIADO"])

        # Salvar a planilha
        wb.save("exemplo.xlsx")

    def log(self,msg):
        self.main_view.log.append(msg)
        self.main_view.log.ensureCursorVisible()









    

        
