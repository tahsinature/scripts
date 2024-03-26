import sys
import uuid
import click


def exec(suffix: str, domain: str):
    unique_10_digit = uuid.uuid4().hex[:10]
    final_email = unique_10_digit

    if suffix:
        final_email = f"{unique_10_digit}-{suffix}"

    return f"{final_email}@{domain or 'maildrop.cc'}".lower()


@click.command()
@click.argument("suffix", required=False)
@click.argument("domain", required=False, default="maildrop.cc")
def main(suffix: str, domain: str):
    print(exec(suffix, domain))


if __name__ == "__main__":
    main()
