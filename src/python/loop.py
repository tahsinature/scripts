import click
from utilities.system import run_terminal_command_live
import time


@click.command()
@click.argument('count', type=int, required=True)
@click.argument('command', type=str, required=True)
@click.argument('wait', type=int, default=0)
def main(count: int, command: str, wait: int):
    for i in range(count):
        run_terminal_command_live(command, shell=True)
        time.sleep(wait)


if __name__ == "__main__":
    main()
