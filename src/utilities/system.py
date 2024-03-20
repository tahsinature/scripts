import subprocess


def run_terminal_command(command: str, shell: bool = False) -> str:
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        raise Exception(stderr.decode("utf-8").strip())

    return stdout.decode("utf-8").strip()
