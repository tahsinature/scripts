import logging


def display_code_via_panel(code: str):
    from rich.panel import Panel
    from rich.console import Console

    console = Console()
    console.print(Panel(code, title="Content"))


class Log:
    def __init__(self, file_name: str, log_separator: str = "====="):
        self.file_name = file_name
        file_path = f"logs/{file_name}"
        format = "%(asctime)s - %(message)s"
        if log_separator:
            format += "\n" + log_separator
        logging.basicConfig(filename=file_path, level=logging.DEBUG, format=format)

    def debug(self, message: str):
        logging.debug(message)
