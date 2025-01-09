from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel
from PySide6.QtCore import QDir

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeView Example")
        self.setGeometry(400, 200, 800, 600)

        # Criar um modelo de sistema de arquivos
        file_system_model = QFileSystemModel()
        file_system_model.setRootPath(QDir.rootPath())

        # Criar a visualização de árvore
        tree_view = QTreeView()
        tree_view.setModel(file_system_model)

        # Definir a raiz a ser mostrada (neste caso, o diretório raiz)
        tree_view.setRootIndex(file_system_model.index(QDir.rootPath()))

        # Definir a árvore como o widget central
        self.setCentralWidget(tree_view)

app = QApplication([])
window = MainView()
window.show()
app.exec()
