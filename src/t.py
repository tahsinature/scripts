import click
from utilities.system import run_terminal_command_live


@click.command()
@click.option('--count', type=int, required=True)
@click.option('--command', type=str, required=True)
def main(count: int, command: str):
    for i in range(count):
        output = run_terminal_command_live("ping google.com", shell=True)
        print(output)


if __name__ == "__main__":
    main()
