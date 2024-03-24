#!/bin/env python3

from datetime import timedelta
from utilities.datetime import try_to_parse_date_or_time
import click
import json

from utilities.prompt import ask_confirmation
from utilities.system import run_terminal_command


json_data = """[
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "February 16, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "February 26, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "March 4, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "March 11, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "March 18, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "March 25, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "April 2, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "April 9, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "April 16, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "April 23, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "April 30, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "May 7, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "May 14, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "May 22, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "June 5, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "June 12, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "June 19, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "June 26, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "July 4, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "July 11, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "July 18, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "July 25, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "August 1, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "August 9, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "August 16, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "August 23, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "August 30, 2024" },
  { "Name": "Trash Day: Garbage + Blue + Green", "Date": "September 9, 2024" },
  { "Name": "Trash Day: Blue + Green", "Date": "September 23, 2024" },
  { "Name": "Subscribe New Garbage Calendar", "Date": "September 23, 2024" }
]
"""


@click.command()
def main():
    data = json.loads(json_data)
    reminder_list = "Playground"
    commands = []

    for item in data:
        date = item["Date"]
        name: str = item["Name"]
        colors = []

        if "blue" in name.lower():
            colors.append("🟦")
        if "green" in name.lower():
            colors.append("🟩")
        if "garbage" in name.lower():
            colors.append("⬛")

        title = f"""{name}: {" ".join(colors)}"""
        parsed = try_to_parse_date_or_time(date)
        if parsed is None:
            raise ValueError("Invalid date format. Please provide the date in the format 'February 16, 2024'.")
        six_hours_before = parsed - timedelta(hours=6)
        command = f"""reminders add "{reminder_list}" "{title}" --due-date "{six_hours_before}\""""
        commands.append(command)

    sure = ask_confirmation("Do you want to continue?")
    if sure:
        for command in commands:
            output = run_terminal_command(command, shell=True)
            print(output)


if __name__ == "__main__":
    main()
