import click
import os
from predictor.grpc.result_client import ResultClient
from predictor.data.aggregator.match_goals import MatchGoals


@click.group()
def cli():
    """Statistico Predictor Command Line Application"""
    pass


@cli.command()
@click.argument('name')
def hello(name: str):
    """Enter your name to receive a welcome message"""
    print(f"Hello {name} you are gorgeous")


@cli.command()
@click.argument('season_id')
def season_data(season_id: str):
    """
    Retrieve and parse data for a given season
    """
    host = os.getenv('DATA_SERVER_HOST')
    port = os.getenv('DATA_SERVER_PORT')

    if host is None or port is None:
        print('Host and port are required to executed this command')
        return

    client = ResultClient(host=host, port=port)
    collator = MatchGoals(client=client)

    df = collator.ForSeason(int(season_id))

    filename = './data-files/season-{}.csv'.format(season_id)

    df.to_csv(filename, encoding='utf-8', index=False)

    print('Data saved')
