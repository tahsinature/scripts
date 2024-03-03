import subprocess
from turtle import st
from typing import List, Optional
from rich import prompt


def select_path(path: str):
    dir_select_command = f"gum file {path} --directory"
    process = subprocess.Popen(dir_select_command,
                               shell=True,
                               stdout=subprocess.PIPE,)
    stdout, stderr = process.communicate()
    output = stdout.decode("utf-8").strip()
    return output


def select_from_list(choices: list[str], limit: Optional[int] = None, clear_screen: bool = False):
    new_line_seperated_choices = "\n".join(choices)
    choose_or_filter = "choose"
    if clear_screen:
        choose_or_filter = "filter"

    limit_flag = "--no-limit"
    if limit:
        limit_flag = f"--limit {limit}"

    select_command = f"echo '{new_line_seperated_choices}' | gum {choose_or_filter} {limit_flag}"

    process = subprocess.Popen(select_command,
                               shell=True,
                               stdout=subprocess.PIPE,)

    stdout, stderr = process.communicate()
    output = stdout.decode("utf-8").strip()

    return list(filter(lambda p: p and p.strip(), output.split("\n")))


def exit_with_message(message: str):
    command = f"""gum style --border normal --margin '1' --padding '1 2' --border-foreground 212 "{message}\""""
    subprocess.run(command,
                   shell=True,)
    exit(1)


def ask_number(message: str):
    while True:
        try:
            return int(prompt.IntPrompt.ask(message))
        except ValueError:
            exit_with_message("You didn't enter a number")


def ask_file(path: str, program: Optional[str] = None):
    selected_program = program
    output = ""

    if not selected_program:
        selected_program = select_from_list(["gum", "ranger", "fd | fzf", "nnn"], 1, True)[0]

    if selected_program == "gum":
        command = f"""gum file {path}"""
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,)
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8").strip()
    elif selected_program == "fd | fzf":
        command = f"fd . {path} -d 1 -e mp3 -e ogg | fzf --multi"
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,)
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8").strip()
        pass
    else:
        exit_with_message(f"Program {selected_program} is not implemented yet")

    files = list(filter(lambda p: p and p.strip(), output.split("\n")))
    if not files:
        exit_with_message("No files selected")

    return files
