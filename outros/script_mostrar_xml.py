import sys
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class UIAutomatorParser(QWidget):
    def __init__(self, xml_file):
        super().__init__()

        # Parse o arquivo XML
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Título da janela
        self.setWindowTitle("UIAutomator Parser")

        # Cria o QTreeWidget para exibir os botões
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Elemento", "Texto", "ID", "Posição (Bounds)"])
        self.layout.addWidget(self.tree_widget)

        # Função para popular a árvore com os dados do XML
        self.populate_tree()

    def populate_tree(self):
        for node in self.root.findall('.//node'):
            # Verifica se é um botão
            # if node.attrib.get('class') == 'android.widget.Button':
                # Cria um item de árvore para o botão
                button_item = QTreeWidgetItem(self.tree_widget, [node.attrib.get('class', 'Desconhecido'),
                                                                node.attrib.get('text', 'Sem texto'),
                                                                node.attrib.get('resource-id', 'Sem ID'),
                                                                node.attrib.get('bounds', 'Sem bounds')])

                # Adiciona o item à árvore
                self.tree_widget.addTopLevelItem(button_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Carrega o arquivo XML do uiautomator (substitua pelo caminho do seu arquivo)
    parser = UIAutomatorParser('window_adump.xml')
    parser.show()

    sys.exit(app.exec())
