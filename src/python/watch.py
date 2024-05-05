import subprocess
import signal
import click
from utilities.prompt import exit_with_message, select_fuzzy_from_list
from utilities.dependency import check_depenedency

signal.signal(signal.SIGINT, signal.SIG_DFL)


def select_extentions():
    extentions = ["*", "py", "js", "ts", "go", "java", "c", "cpp", "html", "css",
                  "scss", "json", "xml", "yml", "yaml", "md", "txt", "sh", "rb", "php"]
    return select_fuzzy_from_list(extentions)


@click.command()
@click.argument("user_command", required=True, type=click.STRING)
@click.option('--ext', type=str, default=None, help='Extension value')
@click.option("--delay", default=0, type=click.INT)
def main(user_command: str, ext: str, delay: int):
    check_depenedency("bunx")
    check_depenedency("gum")

    print(user_command, ext, delay)

    selected_extentions = ext.split(",") if ext else select_extentions()

    if not selected_extentions:
        exit_with_message("No extentions selected")

    final_command = f"""bunx nodemon --exec "clear && {user_command}" --ext '{','.join(selected_extentions)}' --delay {delay}"""

    subprocess.run(final_command, shell=True)


if __name__ == "__main__":
    main()
