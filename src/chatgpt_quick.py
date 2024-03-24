import click
from utilities.log import display_markdown
from utilities.openai import ask_gpt_3_with_chat_completions


@click.command()
@click.option('--question', prompt=True)
def main(question: str):
    try:
        system_message = """
You are a helpful assistant designed to output plain text.
"""
        response = ask_gpt_3_with_chat_completions(
            system_message, question)
        if response and type(response) == str:
            display_markdown(response)
        else:
            print("error in logic: response and type(response) == str:")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
