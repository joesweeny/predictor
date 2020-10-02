import pandas as pd
from compiler.data.preprocessing import helpers

GOAL_POINTS = 20


def pre_process_historic_data_set(results: pd.DataFrame) -> pd.DataFrame:
    updated = helpers.apply_historic_elo_ratings(
        df=results,
        historic_elos={team: 1500 for team in results['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=GOAL_POINTS
    )

    return updated


def pre_process_fixture_data(fixture: pd.Series, results: pd.DataFrame) -> pd.Series:
    stats = results[results['season'] == fixture['season']]

    stats = stats.append(fixture)

    calculated = helpers.create_rolling_stats(stats)

    converted = helpers.create_fixture_rows(calculated)

    fixture = converted[-1:].iloc[0]

    updated_fixture = helpers.apply_current_elo_ratings_for_fixture(
        fixture=fixture,
        data=results,
        points=GOAL_POINTS
    )

    return updated_fixture
