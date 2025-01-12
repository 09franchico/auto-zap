from PySide6.QtWidgets import (
    QMainWindow, QApplication, QGridLayout, QTextEdit, QComboBox, QPushButton,
    QTableWidget, QWidget, QVBoxLayout, QProgressBar, QSpinBox
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
        self.progress_bar = QProgressBar()  # Barra de progresso
        self.spin_box = QSpinBox()  # Adicionar widget para números
        self.combo_box_colun_envio_phone = QComboBox()
        self.start_process = QPushButton("Iniciar processo")
        self.stop_process = QPushButton("Parar processo")
        self.combo_box = QComboBox()
        self.table_widget = QTableWidget(0, 0, self)

        # Configurar a barra de progresso
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        # Configurar o spin box
        self.spin_box.setRange(0, 100)  # Definir o intervalo de números
        self.spin_box.setValue(10)  # Valor inicial
        self.spin_box.setSingleStep(1)  # Incremento ou decremento ao clicar nas setas

        # Adicionar a tabela ao layout principal
        self.layout_grid.addWidget(self.table_widget, 1, 1, 5, 1)

        # Criar um layout vertical para agrupar widgets na coluna 2
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.message_text)
        self.right_layout.addWidget(self.progress_bar)  # Adicionar barra de progresso
        self.right_layout.addWidget(self.spin_box)  # Adicionar spin box para números
        self.right_layout.addWidget(self.combo_box_colun_envio_phone)
        self.right_layout.addWidget(self.start_process)
        self.right_layout.addWidget(self.stop_process, alignment=Qt.AlignTop)
        self.right_layout.addWidget(self.combo_box, alignment=Qt.AlignBottom)

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
