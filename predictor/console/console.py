import click


@click.group()
def cli():
    """Statistico Predictor Command Line Application"""
    pass


@cli.command()
@click.argument('name')
def hello(name: str):
    """Enter your name to receive a welcome message"""
    print(f"Hello {name} you are gorgeous")
