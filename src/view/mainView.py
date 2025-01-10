from PySide6.QtWidgets import (
    QMainWindow, 
    QDockWidget, 
    QLabel,
    QWidget,  
    QGridLayout,
    QTreeWidget, 
    QTreeWidgetItem,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QStyle
)
from PySide6.QtCore import Qt


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema BOT")
        self.setGeometry(400, 200, 1250, 600)

        #----------------------------
        self.central_widget = QWidget()
        self.layout_grid = QGridLayout(self.central_widget)

        #----------------------------
        # Widgets
        self.input_field = QLineEdit()
        self.add_button = QPushButton("Iniciar processo")
        self.add_button.setProperty('class','success')
        self.clear_button = QPushButton("Parar processo")
        self.clear_button.setProperty('class','danger')
        self.combo_box = QComboBox()


        #----------------------------
        # Criar tabela
        self.table_widget = QTableWidget(15, 4, self) 
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Email", "Telefone","Mensagem"])
        # self.table_widget.setItem(0, 0, QTableWidgetItem("Row 1, Column 1"))
        # self.table_widget.setItem(0, 1, QTableWidgetItem("Row 1, Column 2"))
        # self.table_widget.setItem(0, 2, QTableWidgetItem("Row 1, Column 3"))
        # self.table_widget.setItem(1, 0, QTableWidgetItem("Row 2, Column 1"))
        # self.table_widget.setItem(2, 0, QTableWidgetItem("Row 3, Column 1"))

        self.table_widget.setColumnWidth(0, 200)
        self.table_widget.setColumnWidth(1, 230)
        self.table_widget.setColumnWidth(2, 200) 
        self.table_widget.setColumnWidth(3, 300) 


        self.label = QLabel("Nenhum nome definido.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)

        #----------------------------
        # Adicionar widgets ao layout
        self.layout_grid.addWidget(self.input_field,1,1)
        self.layout_grid.addWidget(self.add_button,1,2)
        self.layout_grid.addWidget(self.clear_button,2,2,Qt.AlignmentFlag.AlignTop)
        self.layout_grid.addWidget(self.combo_box,2,2,Qt.AlignmentFlag.AlignBottom)
        self.layout_grid.addWidget(self.table_widget,2,1)
        self.layout_grid.addWidget(self.label,3,1)


        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabels(["Automção"])
        self.populate_tree(tree_widget)

        dock1 = QDockWidget("Menus", self)
        dock1.setWidget(tree_widget)
        dock1.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        dock2 = QDockWidget("Logs", self)
        dock2.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock2.setFixedHeight(100) 
        self.addDockWidget(Qt.BottomDockWidgetArea, dock2)


        stastus_bar = self.statusBar()
        stastus_bar.showMessage("-------------")

        self.setCentralWidget(self.central_widget)
        # self.setFixedSize(self.width(),self.height())

    def update_label(self, text):
        self.label.setText(text)


    def populate_tree(self, tree_widget):
        save_pixmap = QStyle.StandardPixmap.SP_TitleBarMenuButton
        save_icon = self.style().standardIcon(save_pixmap)

        #----------------------------------
        parent_item = QTreeWidgetItem(tree_widget, ["Msg Telegram"])
        parent_item.setIcon(0, save_icon)

        child1 = QTreeWidgetItem(parent_item, ["Filho 1.1"])
        QTreeWidgetItem(child1, ["Neto 1.1.1"])
        QTreeWidgetItem(child1, ["Neto 1.1.2"])

        QTreeWidgetItem(parent_item, ["Filho 1.2"])
        QTreeWidgetItem(parent_item, ["Filho 1.3"])
        QTreeWidgetItem(parent_item, ["Filho 1.4"])

        #----------------------------------
        parent_item2 = QTreeWidgetItem(tree_widget, ["Msg Whats"])
        parent_item2.setIcon(0, save_icon)
        QTreeWidgetItem(parent_item2, ["Filho 2.1"])
        QTreeWidgetItem(parent_item2, ["Filho 2.2"])
        QTreeWidgetItem(parent_item2, ["Filho 2.3"])
        QTreeWidgetItem(parent_item2, ["Filho 2.4"])
        QTreeWidgetItem(parent_item2, ["Filho 2.5"])

       #----------------------------------
        parent_item3 = QTreeWidgetItem(tree_widget, ["Outros"])
        parent_item3.setIcon(0, save_icon)
        QTreeWidgetItem(parent_item3, ["Filho 3.1"])
        QTreeWidgetItem(parent_item3, ["Filho 3.2"])

        tree_widget.expandAll()












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