from  src.model.mainModel import MainModel
from src.view.mainView import MainView
from src.view.secondView import SecondView
from src.view.tableView import TableView
from styles import SetupTheme
from openpyxl import Workbook
from openpyxl import load_workbook



class MainController:
    
    def __init__(self):
        #----------------------------
        # Instanciar o Model e a View
        self.main_model = MainModel()
        self.main_view = MainView()
        self.theme = SetupTheme()
        self.theme.setupTheme('dark')
        self.theme_select()

        #-------------------------
        self.setup_connections()
        self.main_view.show()


    def theme_select(self):
        self.main_view.combo_box.addItems(self.theme.getTheme())


    def setup_connections(self):
        self.main_view.start_process.clicked.connect(self.start_process)
        self.main_view.stop_process.clicked.connect(self.stop_process)
        self.main_view.combo_box.currentTextChanged.connect(self.theme.setupTheme)


    def start_process(self):
        data_plan = self.get_planilha()
        self.main_view.show_table_widget_view(data=data_plan)


    def stop_process(self):
        self.main_view.table_widget.clearContents()

    def get_planilha(self):
        try:
            workbook = load_workbook('exemplo.xlsx')
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









    

        
