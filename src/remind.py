import time
import requests
import json
import click


now = time.time()
expected_formats = "20 Sep | 20 September 2023 | 20 Sep 10:00 pm | 20 September 2023 10:00 pm"
human_readable_time = time.strftime("%d %b %Y %I:%M %p", time.localtime(now))
print(f"Human readable time: {human_readable_time}")


# @click.command()
# @click.option("--reminder", prompt="What do you want to be reminded of?")
# @click.option("--time", prompt="When do you want to be reminded?")
# def exec(reminder, time):
#     # ask_gpt_3_with_chat_completions
#     print(f"Ok, I'll remind you to {reminder} at {time}.")


# if __name__ == "__main__":
#     exec()
