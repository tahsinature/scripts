import json
import click

from utilities.datetime import calculate_time, convert_to_different_tz
from utilities.dependency import check_dependencies
from utilities.openai import ask_gpt_3_with_chat_completions
from utilities.system import run_terminal_command
from utilities.log import Log


check_dependencies(["reminders"], silent=True)
my_timezone = "America/New_York"
reminder_list = "Remind"


system_prompt = """You're a helpful AI assistant that will take user input and try to extract a title & time-data from it. If there is no time involved, give me just the title.
Your json response format should be like this:
    - {{"title":"title","when":{"time":"10:00 pm","timezone":"America/Los_Angeles","date":"20 Sep 2023","date_type":"absolute"}}}
    - {{"title":"title","when":{"time":"10:00 pm","timezone":"America/Los_Angeles","date":1,"date_type":"relative"}}} // unit: days. 0 means no date / today. 1 means tomorrow. -1 means yesterday / 5 means 5 days from now / -5 means 5 days ago and so on.
when {
    time: "python %I:%M %p" # required # do your best guess and put in proper format. If no time, just put "00:00 am"
    timezone: "America/Los_Angeles" # required # Default: America/New_York
    date: "DD MMM YYYY" | int # required
    date_type: "absolute" | "relative" # required
}
You will give me minified json response.
"""

log = Log("remind")


@click.command()
@click.argument("input", type=str)
def exec(input: str):
    log.group(f"input: {input}")
    res = ask_gpt_3_with_chat_completions(system_prompt, input, "json")
    print(res)
    log.group(f"api_res: {res}")

    if res and type(res) == str:
        dict_res = json.loads(res)
        title = dict_res.get("title")
        when = dict_res.get("when")

        if not title:
            print("Title is required")
            return

        command = f"reminders add {reminder_list} {title}"

        if when:
            requested_tz = when.get("timezone")
            time = when.get("time")
            date = when.get("date")
            date_type = when.get("date_type")
            actual_date = calculate_time(time, requested_tz, date, date_type)
            result = convert_to_different_tz(actual_date, my_timezone)
            command += f""" --due-date "{result}" """

        log.group(f"command: {command}")
        output = run_terminal_command(command, shell=True)
        log.group(f"output: {output}")
        print(output)
    else:
        raise Exception("Invalid response from GPT-3")

    log.end_group()


if __name__ == "__main__":
    exec()
