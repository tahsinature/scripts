import requests
import json
import click


@click.command()
def exec():
    url = "https://icanhazdadjoke.com"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    print(json_data["joke"])


if __name__ == "__main__":
    exec()
