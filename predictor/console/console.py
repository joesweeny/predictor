import click
import os
from predictor.grpc.result_client import ResultClient
from predictor.grpc.team_stats_client import TeamStatsClient
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

    result_client = ResultClient(host=host, port=port)
    team_stats_client = TeamStatsClient(host=host, port=port)
    collator = MatchGoals(
        result_client=result_client, 
        team_stats_client=team_stats_client
    )

    df = collator.for_season(int(season_id))

    filename = './data-files/season-{}.csv'.format(season_id)

    df.to_csv(filename, encoding='utf-8', index=False)

    print('Data saved')
