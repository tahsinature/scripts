import inflect
import click


@click.command()
@click.option('--number', prompt=True)
def spell_big_number(number: str):
    p = inflect.engine()
    w = p.number_to_words(number)
    print(w)


if __name__ == "__main__":
    spell_big_number()
