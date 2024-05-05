import utilities.text as text
import click


@click.command()
@click.argument("env_input", required=False, )
def main(env_input: str):
    if not env_input:
        env_input = click.get_text_stream(
            'stdin').read()

    dict = text.get_env_vars_from_lines(env_input)
    print(text.dict_to_env_semi_colon_seperated(dict))


if __name__ == "__main__":
    main()
