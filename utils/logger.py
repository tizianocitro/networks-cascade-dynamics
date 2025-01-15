import re
import os
from utils.os import str_to_bool

LOGGING_ENABLED = "True"
ANSI_COLOR_PATTERN = re.compile(r'\033\[[0-9;]*m')


def log_important(text="", file_dir="logs", file_path="log"):
    log_to_console(text)
    log_to_file(text, file_dir, file_path)


def log(text="", enabled=True, file_dir="logs", file_path="log"):
    console_enabled = str_to_bool(os.getenv("LOG_CONSOLE_ENABLED", LOGGING_ENABLED)) and enabled
    if console_enabled:
        log_to_console(text)

    file_enabled = str_to_bool(os.getenv("LOG_FILE_ENABLED", LOGGING_ENABLED)) and enabled
    if file_enabled:
        log_to_file(text, file_dir, file_path)


def log_to_file(text, file_dir="logs", file_path="log"):
    file_dir = os.getenv("LOG_FILE_DIR", file_dir)
    file_path = os.getenv("LOG_FILE_PATH", file_path)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file_path = os.path.join(file_dir, f"log_{file_path}.txt")

    plain_text = ANSI_COLOR_PATTERN.sub('', text)
    with open(file_path, "a") as log_file:
        log_file.write(plain_text + "\n")


def log_to_console(text):
    print(text)