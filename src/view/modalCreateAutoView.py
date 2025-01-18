
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import  (
        QWidget, 
        QVBoxLayout,
        QTreeWidget, 
        QTreeWidgetItem,
        QPushButton,
        QLabel,
        QGridLayout,
        QFileDialog,
     )
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ModalCreateAutoView(QWidget):

    def __init__(self):
        super().__init__()

        self.root = None 

        #grid principal tem que tem o parent (Tela)
        self.layout_grid_principal = QGridLayout(self)


        #---------------------------------------
        self.layout_left_phone = QGridLayout()
        self.image_label = QLabel("[  Imagem mobile em analise  ]")
        self.layout_left_phone.addWidget(self.image_label, 0, 0, 2,1)

        #---------------------------------------
        self.layout = QVBoxLayout()
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels([ "Texto", "Posição (Bounds)"])
        self.tree_widget.setColumnWidth(0,300)
        self.tree_widget.setColumnWidth(1,200)
        # self.tree_widget.setColumnWidth(4,200)
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

    def set_image_screen(self,img):

        pixmap = QPixmap("cropped_image.png") 
        desired_width = 400
        desired_height = 450
        pixmap = pixmap.scaled(
             desired_width, 
             desired_height, 
             Qt.AspectRatioMode.KeepAspectRatio, 
             Qt.TransformationMode.SmoothTransformation
             )
        
        self.image_label.setPixmap(pixmap)

    def set_file_xml(self):
        try:
            self.tree = ET.parse("window_dump.xml")
            self.root = self.tree.getroot()
            self.populate_tree()
        except ET.ParseError:
            print("ERRO no set_file_xml")
            self.root = None 

    def open_action_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Arquivos Excel (*.xml)")
        file_dialog.setViewMode(QFileDialog.List)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return None
    

    def populate_tree(self):

        self.tree_widget.clear()
        
        if self.root is not None:
            for node in self.root.findall(".//node"):
                button_item = QTreeWidgetItem(
                    self.tree_widget,
                    [
                        # node.attrib.get("class", "Desconhecido"),
                        node.attrib.get("text", "Sem texto"),
                        # node.attrib.get("resource-id", "Sem ID"),
                        node.attrib.get("bounds", "Sem bounds"),
                    ],
                )

                self.tree_widget.addTopLevelItem(button_item)
        else:
            empty_item = QTreeWidgetItem(
                self.tree_widget, ["-", "-", "-", "-"]
            )
            self.tree_widget.addTopLevelItem(empty_item)