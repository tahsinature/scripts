#!/bin/env python3

from datetime import timedelta
from utilities.datetime import try_to_parse_date_or_time
import click
import json

from utilities.log import display_markdown
from utilities.prompt import ask_confirmation
from utilities.system import run_terminal_command


text_data = """
Python does not have a built-in switch case statement like some other programming languages. However, you can achieve similar functionality using a dictionary. Here's an example:

```python
def switch_case(argument):
    switcher = {
        1: "Case 1",
        2: "Case 2",
        3: "Case 3"
    }

    return switcher.get(argument, "Invalid case")

# Test the function
print(switch_case(1))  # Output: Case 1
print(switch_case(4))  # Output: Invalid case
```

In this example, the `switch_case` function emulates a switch case statement by using a dictionary where keys represent cases and values represent corresponding actions. The `get` method is used to retrieve the value for a given key, falling back to a default value if the key is not found."""


@click.command()
def main():
    display_markdown(text_data)


if __name__ == "__main__":
    main()
