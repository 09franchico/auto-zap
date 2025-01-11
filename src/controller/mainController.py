from  src.model.mainModel import MainModel
from src.view.mainView import MainView
from styles import SetupTheme
from openpyxl import Workbook
from openpyxl import load_workbook
from src.android.androidDeviceManager import AndroidDeviceManager
from PySide6.QtCore import QThread, Signal



class AdbThread(QThread):

    finished = Signal()
    error = Signal(str)

    def __init__(self, adb_manager, phone_number, message, parent=None):
        super().__init__(parent)
        self.adb_manager = adb_manager
        self.phone_number = phone_number
        self.message = message

    def run(self):
        try:

            self.adb_manager.connect_device()
            self.adb_manager.habiliar_adbkeyboard()
            self.adb_manager.mensagem_whats(self.phone_number, self.message)
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))



class MainController:
    
    def __init__(self):
        #----------------------------
        # Instanciar o Model e a View
        self.main_model = MainModel()
        self.main_view = MainView()
        self.theme = SetupTheme()
        self.theme.setupTheme('dark')
        self.theme_select()

        self.adb = None

        #-------------------------
        self.setup_connections()
        self.main_view.show()


    def theme_select(self):
        self.main_view.combo_box.addItems(self.theme.getTheme())


    def setup_connections(self):
        self.main_view.start_process.clicked.connect(self.start_process)
        self.main_view.stop_process.clicked.connect(self.stop_process)
        self.main_view.open_action.triggered.connect(self.open_action_file)
        self.main_view.combo_box.currentTextChanged.connect(self.theme.setupTheme)

    def open_action_file(self):
        file_path_xlsx = self.main_view.open_action_file()

        if file_path_xlsx is not None:
            data_plan = self.get_planilha(file_path_xlsx)
            self.main_view.show_table_widget_view(data=data_plan)

        
    def start_process(self):
        selected_items = self.main_view.table_widget.selectedIndexes()

        if selected_items:
            index = selected_items[0]
            item = self.main_view.table_widget.item(index.row(), index.column())

            if item:
                print(f"Item selecionado: {item.text()}")
                self.adb = AndroidDeviceManager()
                self.adb_thread = AdbThread(self.adb, "92993160919", item.text())
                
                self.adb_thread.finished.connect(self.on_adb_finished)
                self.adb_thread.error.connect(self.on_adb_error)
                self.adb_thread.start()

            else:
                print("Nenhum item selecionado ou item vazio.")
        else:
            print("Nenhum item selecionado.")


    def on_adb_finished(self):
       print("Comando ADB concluído com sucesso!")

    def on_adb_error(self, error_message):
      print(f"Erro ao executar o comando ADB: {error_message}")


    def stop_process(self):
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









    

        
