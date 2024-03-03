import sys
import subprocess


def check(dependency_name: str, exit_on_missing=True, silent=False):
    cmd = f"which {dependency_name}"
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,)
    stdout, stderr = process.communicate()
    output = stdout.decode("utf-8").strip()

    if output == "":
        if not silent:
            print(f"{dependency_name} is not installed")
        if exit_on_missing:
            sys.exit(1)
    else:
        if not silent:
            print(f"{dependency_name} is installed")


def check_depenedency(dependency_name: str, exit_on_missing=True, silent=False):
    check(dependency_name, exit_on_missing, silent)


def check_dependencies(dependency_names: list, exit_on_missing=True, silent=False):
    for dependency_name in dependency_names:
        check(dependency_name, exit_on_missing, silent)
