import time
import json
import click

from utilities.datetime import convert_to_different_tz
from utilities.dependency import check_dependencies
from utilities.openai import ask_gpt_3_with_chat_completions
from utilities.system import run_terminal_command


check_dependencies(["reminders"], silent=True)


now = time.time()
my_timezone = "America/New_York"
expected_formats = "DD MMM YYYY HH:MM:SS AM/PM"  # 15 Sep 2022 03:45:20 PM
current_formatted_time = time.strftime("%d %b %Y %I:%M:%S %p", time.localtime(now))

system_prompt = f"""You're a helpful AI assistant that will take user input and try to extract a time and title from it. If there is no time, give me just the title.
For the time, I want it in this formats: {expected_formats}. Whichever fits best for the given input.
Now in my system time, it's {current_formatted_time}. My timezone is EST. I'm giving you current time so if user says "remind me in 5 minutes", you can calculate the time.
User might ask you in different timezones, so you will try your best to get the timezon. ex: 'America/Los_Angeles'. If you're confused about the time today or tomorrow, see if the requested time location is in the future or past.
Let's say My system time is 21 Mar 2024 03:14 pm. If user says "remind me to wake her up at 4 am indonesia time", you should understand in indonesia it's already 22 Mar 2024. So you should set the reminder for 22 Mar 2024 4 am.

And for the title, try to format it nicely. If it's "remind me to go to the grocery store", just give me "Go to the grocery store".


Give me json with the title, time & timezone. If there is no time, just give me the title.
Expected output-1: {{"title": "title", "time": "20 Sep 2023 10:00 pm", "timezone": "America/Los_Angeles"}}
Expected output-2: {{"title": "title", "time": null, "timezone": null}}
Expected output-3: {{"title": null, "time": null}}
"""


@click.command()
@click.argument("input", type=str)
def exec(input: str):
    res = ask_gpt_3_with_chat_completions(system_prompt, input, "json")

    if res and type(res) == str:
        dict_res = json.loads(res)
        title = dict_res.get("title")
        requested_tz = dict_res.get("timezone")
        if not title:
            print("Title is required")
            return
        time = dict_res.get("time")
        command = f"reminders add Remind {title}"
        if time and requested_tz:
            result = convert_to_different_tz(time, requested_tz, my_timezone)
            command += f""" --due-date "{result}" """

        output = run_terminal_command(command, shell=True)
        print(output)
    else:
        raise Exception("Invalid response from GPT-3")


if __name__ == "__main__":
    exec()
