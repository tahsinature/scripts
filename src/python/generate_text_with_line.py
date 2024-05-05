import click


@click.command()
@click.argument("num_lines", required=False, default="10")
@click.argument("input_text", required=False, default="Random")
def main(num_lines: str, input_text: str):
    text = ""

    for i in range(1, int(num_lines) + 1):
        line = f"{i}. {input_text}"
        text += line + "\n"

    print(text)


if __name__ == "__main__":
    main()
