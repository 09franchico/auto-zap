from ppadb.client import Client as AdbClient
import time
import cv2
import io
from PIL import Image
import numpy as np


class AndroidDeviceManager:
    def __init__(self, host="127.0.0.1", port=5037):
        """Inicializa o cliente ADB."""
        self.client = AdbClient(host=host, port=port)
        self.device = None

    def connect_device(self):
        """Conecta ao dispositivo usando ADB."""
        
        devices = self.client.devices()
        if not devices:
            print("Nenhum dispositivo conectado.")
            return None

        self.device = devices[0]
        print(f"Dispositivo conectado: {self.device.serial}")
        return self.device

    def get_device_info(self):
        """Obtém informações do dispositivo."""
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None

        version = self.device.shell("getprop ro.build.version.release")
        print(f"Versão do Android: {version}")
        return version

    def open_camera(self):
         if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
         a = self.device.shell(f"am start -a android.media.action.STILL_IMAGE_CAMERA")


    def screen_time_on_5min(self):
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
        
        self.device.shell(f'settings put system screen_off_timeout 300000') # 5 minutos ligado


    def habiliar_adbkeyboard(self):

        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
        self.device.shell(f'ime enable com.android.adbkeyboard/.AdbIME')
        time.sleep(2)
        self.device.shell(f'ime set com.android.adbkeyboard/.AdbIME')

    def reset_adbkeyboard(self):
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
        
        self.device.shell(f'ime reset')

    def execute_click_screen(self,bounds):
        x, y = self.calculate_center(bounds)
        self.click(x,y)

    def dump_screen_xml(self):
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
        
        self.device.shell(f'uiautomator dump')
        self.device.pull(f'/sdcard/window_dump.xml',"window_dump.xml")


    def mensagem_whats(self,numero, msg):

        if not self.device:
            print("Nenhum dispositivo conectado.")
            return False, "Nenhum dispositivo conectado."
        
        self.device.shell(f'am start -a android.intent.action.VIEW -d "https://api.whatsapp.com/send?phone={numero}"')
        self.device.shell("ping 127.0.0.1 -n 3 > nul")
        time.sleep(2)

        x, y=self.calculate_center('[69,1465][504,1483]')
        self.click(x,y)
        time.sleep(1)

        self.device.shell(f'am broadcast -a ADB_INPUT_TEXT --es msg "{msg}"')

        time.sleep(1)

        # result = self.device.screencap()
        # image = Image.open(io.BytesIO(result))
        # image.save("screenshot.png")
        # time.sleep(2)

        # image_path = "what.jpg"
        # x, y = self.image_position(image_path,"screenshot.png")
        # self.click(x, y)

        #envia o arquivo
        x, y =self.calculate_center('[639,1450][708,1483]')
        self.click(x,y)
        time.sleep(1)

        #clica no file
        x, y=self.calculate_center('[504,1455][573,1483]')
        self.click(x,y)

        time.sleep(1)

        #clica em documentos
        x, y=self.calculate_center('[139,1160][217,1238]')
        self.click(x,y)

        time.sleep(1)

        #seleciona o arquivo
        x, y=self.calculate_center('[104,403][335,436]')
        self.click(x,y)

        time.sleep(1)

        #envia o arquivo
        x, y=self.calculate_center('[639,1450][708,1483]')
        self.click(x,y)

        time.sleep(1)

        return True, "scrip executado com sucesso"




    def image_position(self,small_image, big_image):

        img_rgb = cv2.imread(big_image)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(small_image, 0)
        height, width = template.shape[::]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF)
        _, _, top_left, _ = cv2.minMaxLoc(res)
        bottom_right = (top_left[0] + width, top_left[1] + height)
        return (top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2
    
    def click(self,tap_x, tap_y):
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
        self.device.shell(f"input tap {tap_x} {tap_y}")

    
    def calculate_center(self, bounds):
        try:
            bounds = bounds.strip("[]").split("][")
            if len(bounds) != 2:
                raise ValueError("Bounds string format is incorrect. Expected format: '[x1,y1][x2,y2]'")
            
            # Separar e converter as coordenadas
            x1, y1 = map(int, bounds[0].split(","))
            x2, y2 = map(int, bounds[1].split(","))
            
            # Calcular o centro
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y
        except Exception as e:
            raise ValueError(f"Error calculating center: {e}")