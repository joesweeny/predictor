import click
from datetime import datetime, timezone
from predictor.framework.container import Container


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
@click.argument('date_before')
def season_data(season_id: str, date_before: str):
    """
    Retrieve and parse data for a given season
    """
    collator = Container().match_goals_aggregator()

    try:
        date = datetime.fromisoformat(date_before)
    except ValueError:
        print('Date provided is not a valid RFC3339 date')
        return

    df = collator.for_season(season_id=int(season_id), date_before=date)

    filename = './data-files/season-{}.csv'.format(season_id)

    df.to_csv(filename, encoding='utf-8', index=False)

    print('Data saved')


@cli.command()
def process_supported_competitions_data():
    """
    Parse and save data for supported competitions
    """
    handler = Container().data_handler()

    now = datetime.now(timezone.utc).replace(microsecond=0)

    handler.store_match_goals_data_for_supported_competitions(
        date_before=now
    )

    print('Data saved')


# Remove this command once preprocessing and model work is complete
@cli.command()
@click.argument('fixture_id')
def process_feature_data(fixture_id):
    predictor = Container().match_goals_predictor()

    p = predictor.predict_for_fixture(fixture_id=int(fixture_id))

    print(p)


@cli.command()
def pre_process_match_goals_data_for_supported_competitions():
    container = Container()

    competitions = container.get_config().SUPPORTED_COMPETITIONS

    for i, competition in competitions.items():
        df = container.match_goals_pre_processor().pre_process_feature_data_for_competition(competition['id'])

        filename = './data-files/competition-{}.csv'.format(competition['id'])

        df.to_csv(filename, encoding='utf-8', index=False)

    print('Competition PreProcessing Complete')
