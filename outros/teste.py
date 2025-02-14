import re

# Nome do arquivo onde os eventos foram salvos
file_path = "movimentos_touchscreen.txt"

# Regex para capturar coordenadas X e Y
event_regex = re.compile(r"0035 (\w+)|0036 (\w+)")

with open(file_path, "r") as file:
    for line in file:
        match = event_regex.search(line)
        if match:
            x = int(match.group(1), 16) if match.group(1) else None
            y = int(match.group(2), 16) if match.group(2) else None
            if x is not None:
                print(f"Eixo X: {x}")
            if y is not None:
                print(f"Eixo Y: {y}")
