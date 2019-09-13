import click
from datetime import datetime, timezone
from compiler.framework.container import Container


@click.group()
def cli():
    """Statistico Odds Compiler Command Line Application"""
    pass


@cli.command()
def pre_process_match_goals_data_for_supported_competitions():
    """
    Parse and save data for supported competitions
    """
    handler = Container().data_handler()

    now = datetime.now(timezone.utc).replace(microsecond=0)

    handler.store_match_goals_data_for_supported_competitions(
        date_before=now
    )

    print('Match Goals data pre processing complete')

