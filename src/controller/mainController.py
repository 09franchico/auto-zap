from  src.model.mainModel import MainModel
from src.view.mainView import MainView
from src.view.secondView import SecondView
from src.view.tableView import TableView
from styles import SetupTheme



class MainController:
    
    def __init__(self):
        #----------------------------
        # Instanciar o Model e a View
        self.main_model = MainModel()
        self.main_view = MainView()
        self.theme = SetupTheme()
        self.theme.setupTheme('dark')

        self.theme_select()
        self.setup_connections()

        self.main_view.show()


    def theme_select(self):
        self.main_view.combo_box.addItems(self.theme.getTheme())


    def setup_connections(self):
        self.main_view.add_button.clicked.connect(self.add_name)
        self.main_view.clear_button.clicked.connect(self.clear_name)
        self.main_view.combo_box.currentTextChanged.connect(self.theme.setupTheme)


    def add_name(self):
        name = self.main_view.input_field.text()
        if name:
            self.main_model.addNome(name)
            self.main_view.update_label(name)

    def clear_name(self):
        self.main_model.removeNome()
        self.main_view.update_label("Nenhum nome definido.")







    

        
