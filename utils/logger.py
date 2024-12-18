import re
import os

ANSI_COLOR_PATTERN = re.compile(r'\033\[[0-9;]*m')

def log(text="", enabled=True, file_dir="logs", file_path="log"):
    if enabled:
        print(text)

        file_dir = os.getenv("LOG_FILE_DIR", file_dir)
        file_path = os.getenv("LOG_FILE_PATH", file_path)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_path = os.path.join(file_dir, f"log_{file_path}.txt")

        plain_text = ANSI_COLOR_PATTERN.sub('', text)
        with open(file_path, "a") as log_file:
            log_file.write(plain_text + "\n")