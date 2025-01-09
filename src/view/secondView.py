from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class SecondView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Second View")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Second view is active!")
        self.layout.addWidget(self.label)

        self.close_button = QPushButton("Close")
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        #--------------------------
        self.close_button.clicked.connect(self.handle_close)

    def handle_close(self):
        self.close()