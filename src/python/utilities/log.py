import logging
from os import path
from typing import List
from utilities.config import log_dir
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel


def display_code_via_panel(code: str):
    console = Console()
    console.print(Panel(code, title="Content"))


def display_markdown(markdown: str):

    console = Console()
    console.print(Markdown(markdown))


def gen_unique_id():
    import uuid
    return str(uuid.uuid4())


class Log:

    def __init__(self, file_name: str):
        self.__group_logs: List[str] = []
        logger_name = f"logger-{gen_unique_id()}"
        logger = logging.getLogger(logger_name)
        if not file_name.endswith(".log"):
            file_name += ".log"

        file_path = path.join(log_dir, file_name)
        format = """========== 🆕 %(asctime)s 🆕 ==========
%(message)s
========== 🔚 %(asctime)s 🔚 =========="""
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(logging.Formatter(format))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        self.logger = logger

    def debug(self, message: str):
        self.logger.debug(message)

    def group(self, message: str):
        self.__group_logs.append(message)

    def end_group(self):
        msg = "\n".join(self.__group_logs)
        self.logger.debug(msg)
