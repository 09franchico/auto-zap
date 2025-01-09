from PySide6.QtWidgets import  QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class TableView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableWidget Example")
        self.setGeometry(100, 100, 600, 400)

        # Configuração do widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Criar tabela
        self.table_widget = QTableWidget(3, 3, self)  # 3 linhas, 3 colunas
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        
        # Adicionar dados
        self.table_widget.setItem(0, 0, QTableWidgetItem("Row 1, Column 1"))
        self.table_widget.setItem(0, 1, QTableWidgetItem("Row 1, Column 2"))
        self.table_widget.setItem(0, 2, QTableWidgetItem("Row 1, Column 3"))
        self.table_widget.setItem(1, 0, QTableWidgetItem("Row 2, Column 1"))
        self.table_widget.setItem(2, 0, QTableWidgetItem("Row 3, Column 1"))

        # Layout
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.table_widget)