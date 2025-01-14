import click


@click.command()
@click.option("--max_tokens", default=1024, help="Maximum tokens to generate.")
def main(max_tokens):
    from web import Web

    Web(max_tokens=max_tokens).run()


if __name__ == "__main__":
    main()
