from PySide6.QtWidgets import (
    QMainWindow, 
    QTextEdit, 
    QDockWidget, 
    QLabel,
    QWidget, 
    QVBoxLayout, 
    QTreeWidget, 
    QTreeWidgetItem,
    QLineEdit,
    QPushButton
)
from PySide6.QtCore import Qt


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 - Tree")
        self.setGeometry(100, 100, 1200, 600)

        #----------------------------
        # Layout principal
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        #----------------------------
        # Widgets
        self.input_field = QLineEdit()
        self.add_button = QPushButton("Adicionar Nome")
        self.add_button.setProperty('class','success')
        self.add_button.setProperty('class', 'big_button')
        self.clear_button = QPushButton("Limpar Nome")
        self.clear_button.setProperty('class','danger')
        self.open_second_view_button = QPushButton("Open Second View")
        self.label = QLabel("Nenhum nome definido.")

        #----------------------------
        # Adicionar widgets ao layout
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.open_second_view_button)
        self.layout.addWidget(self.label)

        self.setCentralWidget(self.central_widget)

    def update_label(self, text):
        self.label.setText(text)












    #-----------------------------------------------------------------

    #     central_widget = QTextEdit()
    #     central_widget.setPlaceholderText("Área de texto principal")
    #     self.setCentralWidget(central_widget)
    #     self.create_docks()


    # def create_docks(self):

    #     #-----------------------------------------------
    #     dock1 = QDockWidget("Painel 1 - TreeView", self)
    #     dock1.setAllowedAreas(Qt.AllDockWidgetAreas)


    #     tree_widget = QTreeWidget()
    #     tree_widget.setHeaderLabels(["Nome"])
    #     self.populate_tree(tree_widget)

    #     dock1.setWidget(tree_widget)
    #     self.addDockWidget(Qt.LeftDockWidgetArea, dock1)


    #     #-----------------------------------------------
    #     dock2 = QDockWidget("Painel 2", self)
    #     dock2.setAllowedAreas(Qt.AllDockWidgetAreas)
    #     dock2.setWidget(QLabel("Conteúdo do Painel 2"))
    #     self.addDockWidget(Qt.RightDockWidgetArea, dock2)

    #     #-----------------------------------------------
    #     dock3 = QDockWidget("Painel 3", self)
    #     dock3.setAllowedAreas(Qt.AllDockWidgetAreas)

    #     custom_widget = QWidget()
    #     layout = QVBoxLayout()
    #     layout.addWidget(QLabel("Painel com layout personalizado"))
    #     layout.addWidget(QTextEdit("Campo de texto no Painel 3"))
    #     custom_widget.setLayout(layout)

    #     dock3.setWidget(custom_widget)
    #     self.addDockWidget(Qt.BottomDockWidgetArea, dock3)
    #     dock3.setFloating(False)



    # def populate_tree(self, tree_widget):
    #     parent_item = QTreeWidgetItem(tree_widget, ["Item Pai 1"])
    #     QTreeWidgetItem(parent_item, ["Filho 1.1"])
    #     QTreeWidgetItem(parent_item, ["Filho 1.2"])
    #     parent_item2 = QTreeWidgetItem(tree_widget, ["Item Pai 2"])
    #     QTreeWidgetItem(parent_item2, ["Filho 2.1"])
    #     QTreeWidgetItem(parent_item2, ["Filho 2.2"])

    #     parent_item3 = QTreeWidgetItem(tree_widget, ["Item Pai 3"])
    #     QTreeWidgetItem(parent_item3, ["Filho 3.1"])
    #     QTreeWidgetItem(parent_item3, ["Filho 3.2"])


    #     tree_widget.expandAll()