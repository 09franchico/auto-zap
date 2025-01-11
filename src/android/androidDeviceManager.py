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

    def check_wifi_status(self):
        """Verifica se o Wi-Fi está ativado e funcionando."""
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None

        print("Verificando o status do Wi-Fi...")
        wifi_state = self.device.shell("dumpsys wifi | grep 'Wi-Fi is'")

        print("TESTE ------------- ",wifi_state)
        if "enabled" in wifi_state:
            print("O Wi-Fi está habilitado.")
        else:
            print("O Wi-Fi está desabilitado.")

        connection_info = self.device.shell("dumpsys wifi | grep 'Connected to'")

        print("-------------",connection_info)
        if connection_info:
            print("O dispositivo está conectado a uma rede Wi-Fi:")
            print(connection_info.strip())
        else:
            print("O dispositivo não está conectado a nenhuma rede Wi-Fi.")

    def start_screen_recording(self, file_path="/sdcard/video.mp4", duration=30):
        """Grava a tela do dispositivo por um determinado tempo e salva o vídeo no dispositivo."""
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None

        print(f"Iniciando gravação de tela para {duration} segundos...")
        self.device.shell(f"screenrecord --time-limit {duration} {file_path}")
        time.sleep(duration)
        print(f"Gravação concluída. Baixando o vídeo para o computador...")
        self.device.pull(file_path, "video.mp4")
        print("Vídeo salvo como video.mp4")

    def open_camera(self):

         if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
         
         a = self.device.shell(f"am start -a android.media.action.STILL_IMAGE_CAMERA")

         print("------------------------- ",a)


    def volte_call_test(self, phone_number, audio_file="/sdcard/call_audio.wav"):
        """
        Realiza um teste de chamada MO VoLTE:
        - Faz uma chamada para o número fornecido.
        - Mantém a chamada conectada por 20 segundos.
        - Grava o áudio da chamada, se possível.
        - Desconecta a chamada e aguarda 10 segundos.
        - Repete o processo por 2 ciclos.
        """
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None

        for cycle in range(2):
            print(f"Iniciando o ciclo {cycle + 1} de teste de chamada...")

            # Fazer a chamada
            print(f"Chamando {phone_number}...")
            self.device.shell(f"am start -a android.intent.action.CALL -d tel:{phone_number}")
            time.sleep(2)  # Aguarda para iniciar a gravação

            # Iniciar gravação de áudio
            print("Iniciando gravação de áudio...")
            self.device.shell(f"am start -a android.media.action.RECORD_AUDIO -d {audio_file}")

            # Aguarda 20 segundos com a chamada conectada
            time.sleep(20)

            # Parar gravação de áudio
            print("Parando gravação de áudio...")
            self.device.shell("input keyevent KEYCODE_STOP")

            # Baixar o arquivo de áudio para o computador
            local_audio_file = f"call_audio_cycle_{cycle + 1}.wav"
            print(f"Baixando o arquivo de áudio como {local_audio_file}...")
            self.device.pull(audio_file, local_audio_file)

            # Desconectar a chamada
            print("Desconectando a chamada...")
            self.device.shell("input keyevent 6")  # Keyevent 6 é o código para 'END CALL'
            time.sleep(10)  # Aguarda 10 segundos antes do próximo ciclo

        print("Teste de chamada MO VoLTE concluído.")


    def volte_call_test_mt(self, accept_call=True, cycles=2):
        """
        Realiza um teste de chamada MT VoLTE:
        - Aguarda uma chamada de entrada.
        - Aceita a chamada (se `accept_call` for True).
        - Mantém a chamada conectada por 20 segundos.
        - Desconecta a chamada e aguarda 10 segundos.
        - Repete o processo pelo número de ciclos especificado.
        """
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None

        for cycle in range(cycles):
            print(f"Iniciando o ciclo {cycle + 1} de teste de chamada MT...")

            # Simular a chegada de uma chamada (esta parte depende de simulação externa ou cenário real)
            print("Aguardando chamada de entrada...")

            # Aguarda até que uma chamada seja recebida (substituir por lógica real para detecção de chamada)
            # Aqui usamos um atraso para representar o tempo de espera
            time.sleep(5)

            if accept_call:
                # Aceitar a chamada
                print("Aceitando a chamada...")
                self.device.shell("input keyevent 5")  # Keyevent 5 é o código para 'ANSWER CALL'

                # Aguarda 20 segundos com a chamada conectada
                time.sleep(20)

                # Desconectar a chamada
                print("Desconectando a chamada...")
                self.device.shell("input keyevent 6")  # Keyevent 6 é o código para 'END CALL'

            # Aguarda 10 segundos antes do próximo ciclo
            time.sleep(10)

        print("Teste de chamada MT VoLTE concluído.")


    def ps_253_test(self, phone_number, test_duration=2):
        """
        Realiza o teste PS-2.5.3:
        1. Configura tethering no dispositivo.
        2. Faz uma chamada CS para o Cliente 1.
        3. Inicia o throughput bidirecional UDP.
        4. Mede a média de throughput de downlink e uplink por 10 minutos.
        
        Args:
            phone_number (str): Número para fazer a chamada CS.
            test_duration (int): Duração do teste de throughput em segundos (padrão: 600).
        """
        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None

        print("Iniciando o teste PS-2.5.3...")

        # Passo 1: Ativar tethering
        print("Ativando tethering USB/Wi-Fi...")
        tethering_result = self.device.shell("svc wifi enable && settings put global tether_dun_required 0")
        if "error" in tethering_result:
            print("Erro ao ativar tethering.")
            return

        # Passo 2: Fazer uma chamada CS
        print(f"Chamando {phone_number}...")
        self.device.shell(f"am start -a android.intent.action.CALL -d tel:{phone_number}")
        time.sleep(5)  # Tempo para iniciar a chamada

        # Verificar se a chamada foi conectada
        call_status = self.device.shell("dumpsys telephony.registry | grep 'mCallState'")
        if "mCallState=0" not in call_status:
            print("Erro: A chamada não foi conectada.")
            self.device.shell("input keyevent 6")  # Finalizar chamada, se necessário
            return

        print("Chamada conectada.")

        # Passo 3: Iniciar o throughput bidirecional UDP
        print("Iniciando throughput bidirecional UDP...")
        # Comando fictício - substitua pelo comando real ou integração com ferramenta de teste
        self.device.shell("iperf3 -c 192.168.1.1 -u -b 100M -t 600")  # Exemplo usando iperf3
        print(f"Testando throughput por {test_duration} segundos...")
        time.sleep(test_duration)

        # Passo 4: Medir o throughput
        print("Medindo throughput médio...")
        uplink_throughput = self.device.shell("cat /proc/net/dev | grep wlan0 | awk '{print $2}'")
        downlink_throughput = self.device.shell("cat /proc/net/dev | grep wlan0 | awk '{print $10}'")

        uplink_mbps = int(uplink_throughput) / (test_duration * 1024 * 1024)
        downlink_mbps = int(downlink_throughput) / (test_duration * 1024 * 1024)

        print(f"Throughput médio Uplink: {uplink_mbps:.2f} Mbps")
        print(f"Throughput médio Downlink: {downlink_mbps:.2f} Mbps")

        # Passo 5: Comparar desempenho com dispositivo de referência
        print("Comparando desempenho com dispositivos de referência...")
        # Dados fictícios - substitua pela lógica de comparação apropriada
        reference_uplink = 5.0  # Mbps
        reference_downlink = 10.0  # Mbps

        if uplink_mbps >= reference_uplink and downlink_mbps >= reference_downlink:
            print("Desempenho dentro dos limites esperados.")
        else:
            print("Desempenho abaixo do esperado.")

        # Finalizar chamada
        print("Finalizando chamada CS...")
        self.device.shell("input keyevent 6")  # Finaliza a chamada

        print("Teste PS-2.5.3 concluído.")


    def mensagem_whats(self,numero, msg):

        if not self.device:
            print("Nenhum dispositivo conectado.")
            return None
        
    
        # Abrir o WhatsApp com o número fornecido
        self.device.shell(f'am start -a android.intent.action.VIEW -d "https://api.whatsapp.com/send?phone={numero}"')
        
        # Aguardar 3 segundos
        self.device.shell("ping 127.0.0.1 -n 3 > nul")

        time.sleep(2)
        
        # Digitar a mensagem
        self.device.shell(f'input text "{msg}"')


        result = self.device.screencap()
        image = Image.open(io.BytesIO(result))
        image.save("screenshot.png")

        time.sleep(2)

        image_path = "what.jpg"

        print("----------- Executou -----------------")
        x, y = self.image_position(image_path,"screenshot.png")
        
        # Clicar no botão
        self.click(x, y)


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