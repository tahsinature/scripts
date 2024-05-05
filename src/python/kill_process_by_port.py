import os
import click


def find_pid_by_port(port: int) -> str:
    return os.popen(f"lsof -i :{port} | grep LISTEN | awk '{{print $2}}'").read().strip()


def kill_process_by_pid(pid: str):
    os.system(f"kill {pid}")


def get_process_details_by_pid(pid: str):
    details = os.popen(f"ps -p {pid} -o command=").read().strip()
    focus_part = details.split(" ")[0]
    short_command = focus_part.split("/")[-1]
    return short_command


@click.command()
@click.argument("port", type=int)
@click.option("--prompt / --no-prompt", default=True, help="Prompt before killing")
def main(port: int, prompt: bool):
    pid = find_pid_by_port(port)
    if pid:
        details = get_process_details_by_pid(pid)

        if prompt:
            confirm_message = f"Kill {details}, pid: {pid}, port: {port}?"
            click.confirm(confirm_message, abort=True)

        kill_process_by_pid(pid)
        print(f"Killed {details}, pid: {pid}, port: {port}")
    else:
        print("No process found")


if __name__ == "__main__":
    main()
