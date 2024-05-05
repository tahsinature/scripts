import subprocess


def copy_to_clipboard(text: str):
    process = subprocess.Popen(
        "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE)
    process.communicate(text.encode("utf-8"))


def read_from_clipboard():
    process = subprocess.Popen(
        "pbpaste", env={"LANG": "en_US.UTF-8"}, stdout=subprocess.PIPE)
    return process.communicate()[0].decode("utf-8")
