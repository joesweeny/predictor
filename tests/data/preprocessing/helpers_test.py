import pandas as pd
from compiler.data.preprocessing import helpers


def test_elo_applier_returns_data_frame_with_elo_ratings_applied():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    updated = helpers.apply_historic_elo_ratings(
        df=df,
        historic_elos={team: 1500 for team in df['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=20
    )

    row_1 = updated[updated['fixtureID'] == 10332799].iloc[0]
    row_2 = updated[updated['fixtureID'] == 10332792].iloc[0]

    assert row_1['homeElo'] == 1474.34
    assert row_1['awayElo'] == 1707.93
    assert row_1['homeAttackStrength'] == 1671.59
    assert row_1['homeDefenceStrength'] == 1354.31
    assert row_1['awayAttackStrength'] == 1775.29
    assert row_1['awayDefenceStrength'] == 1442.83

    assert row_2['homeElo'] == 1472.02
    assert row_2['awayElo'] == 1642.73
    assert row_2['homeAttackStrength'] == 1578.95
    assert row_2['homeDefenceStrength'] == 1424.13
    assert row_2['awayAttackStrength'] == 1664.34
    assert row_2['awayDefenceStrength'] == 1441.56


def test_apply_current_elo_ratings_for_fixture_calculates_ratings_and_applies_them_to_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    updated = helpers.apply_current_elo_ratings_for_fixture(
        fixture=fixture,
        data=df,
        points=20
    )

    row = updated.iloc[0, :]

    assert row['homeAttackStrength'] == 1816.55
    assert row['homeDefenceStrength'] == 1526.98
    assert row['awayAttackStrength'] == 1752.04
    assert row['awayDefenceStrength'] == 1395.45


def test_create_rolling_stats_returns_a_dataframe_of_calculated_rolling_stats():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    df = df[(df['season'] == "2017/2018")
            & (df['round'].isin([1, 2, 3, 4]))
            & (df['awayTeam'] == 'West Ham United')]

    stats = helpers.create_rolling_stats(df)

    stats = stats[stats['team'] == 'West Ham United']

    row_2 = stats[stats['fixtureID'] == 1711119].iloc[0]
    row_3 = stats[stats['fixtureID'] == 1710828].iloc[0]

    assert row_2['goalsScored'] == 0
    assert row_2['xGFor'] == 0.63
    assert row_2['shotsOnGoal'] == 1
    assert row_2['shotsTotal'] == 9
    assert row_2['goalsConceded'] == 4
    assert row_2['xGAgainst'] == 2.64

    assert row_3['goalsScored'] == 2
    assert row_3['xGFor'] == 2.16
    assert row_3['shotsOnGoal'] == 9
    assert row_3['shotsTotal'] == 25
    assert row_3['goalsConceded'] == 7
    assert row_3['xGAgainst'] == 4.78


def test_create_fixture_rows_converts_multi_line_stats_into_fixture_rows():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    df = df[(df['season'] == "2017/2018")
            & (df['round'].isin([1, 2, 3, 4]))
            & (df['awayTeam'] == 'West Ham United')]

    stats = helpers.create_rolling_stats(df)

    fixtures = helpers.create_fixture_rows(stats)

    columns = [
        "fixtureID",
        "date",
        "round",
        "season",
        "homeTeam",
        "homeGoalsConceded",
        "homeGoalsScored",
        "homeShotsOnGoal",
        "homeShotsTotal",
        "homeXGA",
        "homeXGF",
        "awayTeam",
        "awayGoalsConceded",
        "awayGoalsScored",
        "awayShotsOnGoal",
        "awayShotsTotal",
        "awayXGA",
        "awayXGF",
    ]

    assert len(fixtures) == 3
    assert (fixtures.columns == columns).all()
