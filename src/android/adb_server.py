import subprocess


class StartDaemon:
    @staticmethod
    def start():
        try:
            # Inicia o servidor ADB
            process = subprocess.run(
                ['platform-tools/adb.exe', 'start-server'],
                capture_output=True, text=True
            )
            if process.returncode == 0:
                print("ADB server iniciado com sucesso!")
                print(process.stdout)
            else:
                print("Falha ao iniciar o ADB server.")
                print(process.stderr)
        except FileNotFoundError:
            print("Erro: O arquivo adb.exe não foi encontrado. Verifique o caminho.")
        except Exception as e:
            print(f"Erro inesperado: {e}")



if __name__ == "__main__":
    StartDaemon.start()