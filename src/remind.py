import time
import json
import click

from utilities.dependency import check_dependencies
from utilities.openai import ask_gpt_3_with_chat_completions
from utilities.system import run_terminal_command

# reminders add Tasks Go to the grocery store --due-date "23 mar 25 8:30:21 pm"

check_dependencies(["reminders"], silent=True)


now = time.time()
expected_formats = "20 Sep | 20 September 2023 | 20 Sep 10:00 pm | 20 September 2023 10:00 pm | 20 Sep 2023 10:00:03 pm"
human_readable_time = time.strftime("%d %b %Y %I:%M %p", time.localtime(now))

system_prompt = f"""You're a helpful AI assistant that will take user input and try to extract a time and title from it. If there is no time, give me just the title.
For the time, I want it in one of these formats: {expected_formats}. Whichever fits best for the given input.
Now in my system time, it's {human_readable_time}. I'm giving you current time so if user says "remind me in 5 minutes", you can calculate the time.

And for the title, try to format it nicely. If it's "remind me to go to the grocery store", just give me "Go to the grocery store".

Give me json with the title and time. If there is no time, just give me the title.
Expected output-1: {{"title": "title", "time": "20 Sep 2023 10:00 pm"}}
Expected output-2: {{"title": "title", "time": null}}
Expected output-3: {{"title": null, "time": null}}
"""


@click.command()
@click.argument("input", type=str)
def exec(input: str):
    res = ask_gpt_3_with_chat_completions(system_prompt, input, "json")

    if res and type(res) == str:
        dict_res = json.loads(res)
        title = dict_res.get("title")
        if not title:
            print("Title is required")
            return
        time = dict_res.get("time")
        command = f"reminders add Remind {title}"
        if time:
            command += f""" --due-date "{time}" """
        output = run_terminal_command(command, shell=True)
        print(output)
    else:
        raise Exception("Invalid response from GPT-3")


if __name__ == "__main__":
    exec()
