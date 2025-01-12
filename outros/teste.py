from PySide6.QtWidgets import (
    QMainWindow, QApplication, QGridLayout, QTextEdit, QComboBox, QPushButton,
    QTableWidget, QWidget, QVBoxLayout
)
from PySide6.QtCore import Qt
import sys

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema BOT")
        self.resize(1250, 700)

        # Configurar o layout central
        self.central_widget = QWidget()
        self.layout_grid = QGridLayout(self.central_widget)

        # Criar os widgets
        self.message_text = QTextEdit()
        self.combo_box_colun_envio_phone = QComboBox()
        self.start_process = QPushButton("Iniciar processo")
        self.stop_process = QPushButton("Parar processo")
        self.combo_box = QComboBox()
        self.table_widget = QTableWidget(0, 0, self)

        # Adicionar a tabela ao layout principal
        self.layout_grid.addWidget(self.table_widget, 1, 1, 5, 1)

        # Criar um layout vertical para agrupar widgets na coluna 2
        self.right_layout = QGridLayout()
        self.right_layout.addWidget(self.message_text,1,1,1,2)
        self.right_layout.addWidget(self.combo_box_colun_envio_phone,2,1)
        self.right_layout.addWidget(self.start_process,2,2)
        self.right_layout.addWidget(self.stop_process,3,2)
        self.right_layout.addWidget(self.combo_box,3,1)

        # Adicionar o layout vertical ao grid principal
        self.layout_grid.addLayout(self.right_layout, 1, 2, 5, 1)

        # Configurar o widget central
        self.setCentralWidget(self.central_widget)

# Inicialização do aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec_())
