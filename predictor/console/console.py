import click
import pandas as pd
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
    client = ResultClient(host='138.68.132.183', port='50051')
    collator = MatchGoals(client=client)

    df = collator.ForSeason(int(season_id))

    filename = './data-files/season-{}.csv'.format(season_id)

    df.to_csv(filename, encoding='utf-8', index=False)

    print('Data saved')
