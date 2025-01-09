from  src.model.mainModel import MainModel
from src.view.mainView import MainView
from src.view.secondView import SecondView
from src.view.tableView import TableView



class MainController:
    
    def __init__(self):
        #----------------------------
        # Instanciar o Model e a View
        self.main_model = MainModel()
        self.main_view = MainView()
        self.second_view = SecondView() 
        self.table_view = TableView()

        self.setup_connections()
        self.setup_connections2()

        self.main_view.show()

    def setup_connections(self):
        self.main_view.add_button.clicked.connect(self.add_name)
        self.main_view.clear_button.clicked.connect(self.clear_name)

    def setup_connections2(self):
        self.main_view.open_second_view_button.clicked.connect(self.open_second_view)

    def add_name(self):
        name = self.main_view.input_field.text()
        if name:
            self.main_model.addNome(name)
            self.main_view.update_label(name)

    def clear_name(self):
        self.main_model.removeNome()
        self.main_view.update_label("Nenhum nome definido.")


    def open_second_view(self):
        self.table_view.show()
        #self.second_view.show()

        # data_from_first_view = self.main_model.nome

        # self.second_view.label.setText(f"Data from MainView: {data_from_first_view}")





    

        
