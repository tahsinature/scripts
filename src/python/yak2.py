from utilities.system import run_terminal_command
from utilities.text import dict_to_aws_cred_file, dict_to_env_semi_colon_seperated, get_env_vars_from_lines
from utilities.clipboard import copy_to_clipboard
from utilities.dependency import check_depenedency
import pexpect
import signal
import os
import subprocess
import click
from utilities.log import display_code_via_panel


from utilities.prompt import exit_with_message, select_from_list, select_fuzzy_from_list

signal.signal(signal.SIGINT, signal.SIG_DFL)

check_depenedency("yak", silent=True)
check_depenedency("gum", silent=True)


def handle_output(type: str, creds: str):
    supported_types = ["unix-export", "jetbrain", "aws-cred-file"]
    if type and type not in supported_types:
        return exit_with_message(
            f"Output type {type} not supported. Supported types are: {supported_types}")

    if type is None:
        choice = select_from_list(supported_types, 1)
        if not choice:
            exit_with_message("No output type selected")
        type = choice[0]

    if type == supported_types[0]:
        copy_to_clipboard(creds)
        print("Unix export copied to clipboard")
    elif type == supported_types[1]:
        dict = get_env_vars_from_lines(creds)
        jetbrain_env = dict_to_env_semi_colon_seperated(dict)
        copy_to_clipboard(jetbrain_env)
        print("Jetbrain env copied to clipboard")
    elif type == supported_types[2]:
        dict = get_env_vars_from_lines(creds)
        dict = {k.lower(): v for k, v in dict.items() if k and v}
        dict_to_aws_cred_file(dict)

    else:
        exit_with_message(f"Output type {type} not supported")


@click.command()
@click.argument('profile', required=False)
@click.argument('output_type', required=False)
def main(profile: str, output_type: str):
    command = "yak -l"
    child = pexpect.spawn(command, timeout=60, encoding='utf-8')

    child.expect(["Okta password", pexpect.EOF], timeout=60)

    if child.after == "Okta password":
        password = os.environ.get("LAPTOP_PASS")
        if not password:
            p_command = """gum input --password --placeholder \"Enter your CARFAX password\""""
            password = subprocess.run(p_command,
                                      shell=True,
                                      stdout=subprocess.PIPE,).stdout.decode("utf-8").strip()

        child.sendline(password)
        child.expect(pexpect.EOF, timeout=60)

    if not type(child.before) == str:
        exit_with_message("No profiles found")
        return

    if not profile:
        profiles = list(map(lambda p: p.strip(), filter(
            lambda p: p and p.strip(), child.before.split("\n"))))
        selected_profiles = select_fuzzy_from_list(profiles, 1)
        if not selected_profiles:
            exit_with_message("No profile selected")
        profile = selected_profiles[0]

    command = f"yak {profile}"
    child = pexpect.spawn(command, timeout=10, encoding='utf-8')

    child.expect(pexpect.EOF)

    if not type(child.before) == str:
        exit_with_message("No credentials found")
        return

    creds = child.before.strip()

    display_code_via_panel(creds)
    handle_output(output_type, creds)


if __name__ == "__main__":
    main()
