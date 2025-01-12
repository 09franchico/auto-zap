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
    QTextEdit,
    QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,QGuiApplication,QTextCursor


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema BOT")
        self.resize(1250, 700)

        self.create_menu_bar()
        # self.center_on_screen()
        self.showMaximized()

        #----------------------------
        self.central_widget = QWidget()
        self.layout_grid = QGridLayout(self.central_widget)

        #----------------------------
        # Widgets
        self.combo_box_colun_envio_phone = QComboBox()
        self.start_process = QPushButton("Iniciar processo")
        self.stop_process = QPushButton("Parar processo")
        self.combo_box = QComboBox()


        #---------------------------- 
        self.table_widget = QTableWidget(0, 0, self)
        self.layout_grid.addWidget(self.table_widget, 1, 1, 3, 1)

        #----------------------------
        # Adicionar widgets ao layout
        self.layout_grid.addWidget(self.combo_box_colun_envio_phone,1,2)
        self.layout_grid.addWidget(self.start_process,2,2)
        self.layout_grid.addWidget(self.stop_process,3,2,Qt.AlignmentFlag.AlignTop)
        self.layout_grid.addWidget(self.combo_box,3,2,Qt.AlignmentFlag.AlignBottom)

        #----------------------------
        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabels(["Automção"])
        self.populate_tree(tree_widget)

        dock1 = QDockWidget("Menus", self)
        dock1.setWidget(tree_widget)
        dock1.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        #----------------------------
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        dock2 = QDockWidget("Logs", self)
        dock2.setWidget(self.log)
        dock2.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock2.setFixedHeight(150) 
        self.addDockWidget(Qt.BottomDockWidgetArea, dock2)


        stastus_bar = self.statusBar()
        stastus_bar.showMessage("Bot")
        self.setCentralWidget(self.central_widget)

    def add_value_combo_box_envio_phone(self,data:list):
        self.combo_box_colun_envio_phone.clear()
        for item in data:
            if item:
               self.combo_box_colun_envio_phone.addItem(item)


    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def get_column_data(self, column_name):
        
        column_index = -1
        for col in range(self.table_widget.columnCount()):
            header_item = self.table_widget.horizontalHeaderItem(col)
            if header_item and header_item.text() == column_name:
                column_index = col
                break

        if column_index == -1:
            print(f"Coluna '{column_name}' não encontrada.")
            return []

        # Obter os dados da coluna
        column_data = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, column_index)
            column_data.append(item.text() if item else "")

        return column_data


    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Arquivo")
        self.open_action = QAction("Abrir", self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)


        save_action = QAction("Salvar", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        exit_action = QAction("Sair", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("Editar")
        cut_action = QAction("Cortar", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copiar", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)

        paste_action = QAction("Colar", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)

       
        help_menu = menu_bar.addMenu("Ajuda")
        about_action = QAction("Sobre", self)
        help_menu.addAction(about_action)


    def open_action_file(self):
        # --------------------------------------
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Arquivos Excel (*.xlsx *.xlsm)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        
        return None
 
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
        
        self.layout_grid.addWidget(self.table_widget, 1, 1, 3, 1)


    def populate_tree(self, tree_widget):
        save_pixmap = QStyle.StandardPixmap.SP_TitleBarMenuButton
        save_icon = self.style().standardIcon(save_pixmap)

        title_pixmap = QStyle.StandardPixmap.SP_FileLinkIcon
        title_icon = self.style().standardIcon(title_pixmap)

        #----------------------------------
        parent_item = QTreeWidgetItem(tree_widget, ["Msg Telegram"])
        parent_item.setIcon(0, save_icon)

        child1 = QTreeWidgetItem(parent_item, ["Filho 1.1"])
        child1.setIcon(0,title_icon)
        neto_child1 = QTreeWidgetItem(child1, ["Neto 1.1.1"]).setIcon(0,title_icon)
        # neto_child1.setIcon(0,title_icon)

        QTreeWidgetItem(child1, ["Neto 1.1.2"]).setIcon(0,title_icon)

        QTreeWidgetItem(parent_item, ["Filho 1.2"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item, ["Filho 1.3"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item, ["Filho 1.4"]).setIcon(0,title_icon)

        #----------------------------------
        parent_item2 = QTreeWidgetItem(tree_widget, ["Msg Whats"])
        parent_item2.setIcon(0, save_icon)
        QTreeWidgetItem(parent_item2, ["Filho 2.1"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item2, ["Filho 2.2"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item2, ["Filho 2.3"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item2, ["Filho 2.4"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item2, ["Filho 2.5"]).setIcon(0,title_icon)

       #----------------------------------
        parent_item3 = QTreeWidgetItem(tree_widget, ["WEB"])
        parent_item3.setIcon(0, save_icon)
        QTreeWidgetItem(parent_item3, ["Filho 3.1"]).setIcon(0,title_icon)
        QTreeWidgetItem(parent_item3, ["Filho 3.2"]).setIcon(0,title_icon)

        tree_widget.expandAll()

    def log_view(self,msg):
        self.log.append(msg)
        self.log.moveCursor(QTextCursor.End)


