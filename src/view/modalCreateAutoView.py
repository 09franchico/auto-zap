
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import  (
        QWidget, 
        QVBoxLayout,
        QPushButton,
        QLabel,
        QGridLayout,
        QFileDialog,
        QGroupBox,
        QTableWidget,
        QTableWidgetItem,
        QMessageBox,
        QStyle,
     )
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import json


class ModalCreateAutoView(QWidget):

    def __init__(self):
        super().__init__()

        self.root = None 

        #grid principal tem que tem o parent (Tela)
        self.layout_grid_principal = QGridLayout(self)


        #---------------------------------------
        self.layout_left_phone = QGridLayout()
        self.image_label = QLabel("[  IMAGEM MOBILE EM ANALISE  ]")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_left_phone.addWidget(self.image_label, 0, 0, 0,0)

        #---------------------------------------
        self.layout = QVBoxLayout()
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Texto", "Posição (Bounds)"])
        self.table_widget.setColumnWidth(0, 300)
        self.table_widget.setColumnWidth(1, 290)
        self.layout.addWidget(self.table_widget)

        self.populate_table()

        #----------------------------------------
        self.group_box_manual = QGroupBox("")
        self.group_box_manual.setProperty("customProperty", "highlighted")
        self.container_action_manual = QGridLayout()

        #-------------------------------------------
        self.group_box_auto = QGroupBox("")
        self.group_box_auto.setProperty("customProperty", "highlighted")
        self.container_action_auto = QGridLayout()

        #-------------------------------------------
        self.group_box_execute = QGroupBox("")
        self.group_box_execute.setProperty("customProperty", "highlighted")
        self.container_execute_clicks = QGridLayout()


        #----------------------------------------
        self.button_print_phone = QPushButton()
        self.button_print_phone.setText('FOTO')
        self.button_action_phone = QPushButton()
        self.button_action_phone.setText('CLICAR')
        self.button_add_bound = QPushButton("ADICIONAR")
        self.button_back_screen = QPushButton("VOLTAR")
        self.button_clear_add = QPushButton("LIMPAR")
        self.button_save_manual = QPushButton("SALVAR")

        #-----------------------------------------
        save_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveAllButton)
        stop_auto_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        gravar_auto_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)


        self.button_auto_click_screen_phone = QPushButton("GRAVAR")
        self.button_auto_click_screen_phone.setIcon(gravar_auto_icon)
        self.button_stop_auto_click_screen_phone = QPushButton("PARAR")
        self.button_stop_auto_click_screen_phone.setIcon(stop_auto_icon)
        self.button_salvar_auto = QPushButton("SALVAR")
        self.button_salvar_auto.setIcon(save_icon)
        self.button_load_file_auto = QPushButton("CARREGAR")
        self.button_execute_bound = QPushButton("EXECUTAR")

        self.container_action_manual.addWidget(self.button_print_phone,0,0)
        self.container_action_manual.addWidget(self.button_action_phone,0,1)
        self.container_action_manual.addWidget(self.button_add_bound,0,2)
        self.container_action_manual.addWidget(self.button_back_screen,2,0)
        self.container_action_manual.addWidget(self.button_clear_add,2,1)
        self.container_action_manual.addWidget(self.button_save_manual,2,2)

        self.container_action_auto.addWidget(self.button_auto_click_screen_phone,0,0)
        self.container_action_auto.addWidget(self.button_stop_auto_click_screen_phone,0,1)
        self.container_action_auto.addWidget(self.button_salvar_auto,1,1)
    

        self.container_execute_clicks.addWidget(self.button_load_file_auto,0,0)
        self.container_execute_clicks.addWidget(self.button_execute_bound,1,0)



        #------------------------
        self.group_box_manual.setLayout(self.container_action_manual)
        self.group_box_auto.setLayout(self.container_action_auto)
        self.group_box_execute.setLayout(self.container_execute_clicks)

        #------------------------------------------
        self.layout_grid_principal.addLayout(self.layout_left_phone, 1, 1,2,1)
        self.layout_grid_principal.addLayout(self.layout, 1, 2, 1, 3)
        self.layout_grid_principal.addWidget(self.group_box_manual, 2, 2, 1, 1)
        self.layout_grid_principal.addWidget(self.group_box_auto, 2, 3, 1, 1)
        self.layout_grid_principal.addWidget(self.group_box_execute,2,4,1,1)
      

    def set_image_screen(self,img):

        pixmap = QPixmap(img) 
        desired_width = 300
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
            self.populate_table()
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
    
    def open_auto_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Arquivos Excel (*.json)")
        file_dialog.setViewMode(QFileDialog.List)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return None
    
    def save_json_click_xy(self,auto_clicks):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar JSON", "", "JSON Files (*.json)")
        if file_path:
            dados_para_salvar = {"clicks_xy": auto_clicks}
            try:
                with open(file_path, "w") as json_file:
                    json.dump(dados_para_salvar, json_file, indent=4)
                QMessageBox.information(self, "Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar o arquivo: {str(e)}")
    
    def populate_table(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        if self.root is not None:
            for node in self.root.findall(".//node"):
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(node.attrib.get("text", "Sem texto")))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(node.attrib.get("bounds", "Sem bounds")))
        else:
            self.table_widget.setRowCount(1)
            self.table_widget.setItem(0, 0, QTableWidgetItem("-"))
            self.table_widget.setItem(0, 1, QTableWidgetItem("-"))

    def add_text_image_label(self,msg):
        self.image_label.setText(msg)