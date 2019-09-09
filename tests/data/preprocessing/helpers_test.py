import pytest
import pandas as pd
from datetime import datetime
from compiler.data.preprocessing import helpers


def test_elo_applier_returns_data_frame_with_elo_ratings_applied():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    updated = helpers.elo_applier(
        df=df,
        historic_elos={team: 1500 for team in df['homeTeam'].unique()},
        soft_reset_factor=0.96,
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
