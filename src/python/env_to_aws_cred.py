import click
import utilities.text as text


@click.command()
@click.argument("env_input")
def main(env_input: str):
    dict = text.get_env_vars_from_lines(env_input)
    dict = {k.lower(): v for k, v in dict.items() if k and v}
    text.dict_to_aws_cred_file(dict)


if __name__ == "__main__":
    main()
