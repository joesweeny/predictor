import click


@click.command()
def cli():
    """Enter a name to receive a welcome message"""
    click.echo('Hello Joe')
