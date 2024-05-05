import subprocess
from typing import AnyStr


def run_terminal_command(command: str, shell: bool = False) -> str:
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        raise Exception(stderr.decode("utf-8").strip())

    return stdout.decode("utf-8").strip()


def run_terminal_command_live(command: str, shell: bool = False):
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    while True and process.stdout:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output.strip():
            print(output.strip())

    return process.poll()
