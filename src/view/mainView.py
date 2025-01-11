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
    QStyle,
    QTextEdit
)
from PySide6.QtCore import Qt


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema BOT")
        self.setGeometry(400, 200, 1250,700)

        #----------------------------
        self.central_widget = QWidget()
        self.layout_grid = QGridLayout(self.central_widget)

        #----------------------------
        # Widgets
        self.start_process = QPushButton("Iniciar processo")
        self.stop_process = QPushButton("Parar processo")
        self.combo_box = QComboBox()


        #----------------------------
        # Criar tabela
        # self.table_widget = QTableWidget(20, 4, self) 
        # self.table_widget.setHorizontalHeaderLabels(["", "", "",""])
        

        # self.table_widget.setColumnWidth(0, 200)
        # self.table_widget.setColumnWidth(1, 230)
        # self.table_widget.setColumnWidth(2, 200) 
        # self.table_widget.setColumnWidth(3, 300) 

        #----------------------------
        # Adicionar widgets ao layout
        self.layout_grid.addWidget(self.start_process,1,2)
        self.layout_grid.addWidget(self.stop_process,2,2,Qt.AlignmentFlag.AlignTop)
        self.layout_grid.addWidget(self.combo_box,2,2,Qt.AlignmentFlag.AlignBottom)

        #----------------------------
        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabels(["Automção"])
        self.populate_tree(tree_widget)

        dock1 = QDockWidget("Menus", self)
        dock1.setWidget(tree_widget)
        dock1.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        #----------------------------
        self.text_edit = QTextEdit()
        dock2 = QDockWidget("Logs", self)
        dock2.setWidget(self.text_edit)
        dock2.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock2.setFixedHeight(100) 
        self.addDockWidget(Qt.BottomDockWidgetArea, dock2)


        stastus_bar = self.statusBar()
        stastus_bar.showMessage("Bot")

        self.setCentralWidget(self.central_widget)
        # self.setFixedSize(self.width(),self.height())

    def update_label(self, text):
        self.label.setText(text)


    def show_table_widget_view(self, data: dict):
        #---------------------------------
        rows = len(data.get('data', []))
        cols = len(data.get('header_label', []))
        
        self.table_widget = QTableWidget(rows, cols, self)
        self.table_widget.setHorizontalHeaderLabels(data.get('header_label'))

        for col_index in range(cols):
            self.table_widget.setColumnWidth(col_index, 200)

        #-----------------------------------
        # Adicionando os dados dinamicamente
        for row_index, row_data in enumerate(data.get('data', [])):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table_widget.setItem(row_index, col_index, item)
        
        self.layout_grid.addWidget(self.table_widget, 1, 1, 2, 1)


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


