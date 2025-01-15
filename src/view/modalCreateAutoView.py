
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import  (
        QWidget, 
        QVBoxLayout,
        QTreeWidget, 
        QTreeWidgetItem,
        QPushButton,
        QLabel
     )


class ModalCreateAutoView(QWidget):


    def __init__(self,xml_file):
        super().__init__()

        #Parse o arquivo XML
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        # self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("UIAutomator Parser")
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Elemento", "Texto", "ID", "Posição (Bounds)"])
        self.layout.addWidget(self.tree_widget)

        self.populate_tree()

    def populate_tree(self):
        for node in self.root.findall('.//node'):
           
                button_item = QTreeWidgetItem(self.tree_widget, [node.attrib.get('class', 'Desconhecido'),
                                                                node.attrib.get('text', 'Sem texto'),
                                                                node.attrib.get('resource-id', 'Sem ID'),
                                                                node.attrib.get('bounds', 'Sem bounds')])

                # Adiciona o item à árvore
                self.tree_widget.addTopLevelItem(button_item)