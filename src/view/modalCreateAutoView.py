
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import  (
        QWidget, 
        QVBoxLayout,
        QTreeWidget, 
        QTreeWidgetItem,
        QPushButton,
        QLabel,
        QGridLayout
     )
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ModalCreateAutoView(QWidget):


    def __init__(self,xml_file):
        super().__init__()

        #Parse o arquivo XML
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

        #grid principal tem que tem o parent (Tela)
        self.layout_grid_principal = QGridLayout(self)


        #---------------------------------------
        self.layout_left_phone = QGridLayout()
        self.image_label = QLabel()
        pixmap = QPixmap(f"C:/Users/franc/OneDrive/Área de Trabalho/DEV/Python/projeto-pyside/screenshot.png") 
        
        desired_width = 300 
        desired_height = 450 
        pixmap = pixmap.scaled(
             desired_width, 
             desired_height, 
             Qt.AspectRatioMode.KeepAspectRatio, 
             Qt.TransformationMode.SmoothTransformation
             )
        
        self.image_label.setPixmap(pixmap)
        self.layout_left_phone.addWidget(self.image_label, 0, 0, 2,1)

        #---------------------------------------
        self.layout = QVBoxLayout()
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Elemento", "Texto", "ID", "Posição (Bounds)"])
        self.layout.addWidget(self.tree_widget)
        self.populate_tree()

        #----------------------------------------
        self.container_action = QGridLayout()

        self.button_print_phone = QPushButton()
        self.button_print_phone.setText('PRINT')

        self.button_action_phone = QPushButton()
        self.button_action_phone.setText('EXECUTAR ACAO')

        self.container_action.addWidget(self.button_print_phone,0,0)
        self.container_action.addWidget(self.button_action_phone,0,1)
        

        self.layout_grid_principal.addLayout(self.layout_left_phone,1,1)
        self.layout_grid_principal.addLayout(self.layout,1,2)
        self.layout_grid_principal.addLayout(self.container_action,2,2)



    def populate_tree(self):
        for node in self.root.findall('.//node'):
           
                button_item = QTreeWidgetItem(self.tree_widget, [node.attrib.get('class', 'Desconhecido'),
                                                                node.attrib.get('text', 'Sem texto'),
                                                                node.attrib.get('resource-id', 'Sem ID'),
                                                                node.attrib.get('bounds', 'Sem bounds')])

                # Adiciona o item à árvore
                self.tree_widget.addTopLevelItem(button_item)