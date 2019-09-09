import pytest
import pandas as pd
from datetime import datetime
from compiler.data.preprocessing import helpers


def test_elo_applier_returns_data_frame_with_elo_ratings_applied():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    updated = helpers.apply_historic_elo_ratings(
        df=df,
        historic_elos={team: 1500 for team in df['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=20
    )

    row_1 = updated[updated['matchID'] == 10332799].iloc[0]
    row_2 = updated[updated['matchID'] == 10332792].iloc[0]

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

    assert row['homeAttackStrength'] == 1816.81
    assert row['homeDefenceStrength'] == 1526.85
    assert row['awayAttackStrength'] == 1752.18
    assert row['awayDefenceStrength'] == 1395.22
