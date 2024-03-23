#!/bin/env python3

from utilities.log import Log
import click
import subprocess
import json
# import logging

# logger1 = logging.getLogger("test")
# logger1.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("test.log")
# file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
# logger1.addHandler(file_handler)
# logger1.debug("Starting the process.")


log1 = Log("test.log")
log2 = Log("test.log")


@click.command()
def main():
    log1.group("Starting the process.")
    log1.group("Checking the dependencies.")
    log1.group("Doing something.")
    log1.end_group()

    log2.group("Starting the process 2.")
    log2.group("Checking the dependencies 2.")
    log2.group("Doing something 2.")
    log2.end_group()


if __name__ == "__main__":
    main()
